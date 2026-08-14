import ast
from typing import Tuple, Optional

def verify_python_syntax(code: str) -> Tuple[bool, Optional[str]]:
    """
    Parses a string of Python code using ast.parse().
    Returns (True, None) if valid Python, or (False, error_message) if invalid.
    """
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        error_msg = f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}\nCode snippet around error: {e.text}"
        return False, error_msg
    except Exception as e:
        return False, f"AST Parsing Error: {str(e)}"

import os
import subprocess
import tempfile
from logger import logger

class SecurityASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Call(self, node):
        # 1. Block eval, exec, __import__
        if isinstance(node.func, ast.Name):
            if node.func.id in {"eval", "exec", "__import__"}:
                self.errors.append(f"Forbidden function call detected: {node.func.id}()")
        
        # 2. Block raw formatted strings inside .execute(text(...))
        # This matches db.execute(text(f"SELECT * FROM users WHERE id = {user_id}"))
        if isinstance(node.func, ast.Attribute) and node.func.attr == "execute":
            if node.args and isinstance(node.args[0], ast.Call):
                inner_call = node.args[0]
                if isinstance(inner_call.func, ast.Name) and inner_call.func.id == "text":
                    if inner_call.args:
                        arg = inner_call.args[0]
                        # Check if it's an f-string (JoinedStr) or uses .format()
                        if isinstance(arg, ast.JoinedStr):
                            self.errors.append("Potential SQL Injection: f-string used inside text() block.")
                        elif isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute) and arg.func.attr == "format":
                            self.errors.append("Potential SQL Injection: .format() used inside text() block.")
                        elif isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                            self.errors.append("Potential SQL Injection: raw string concatenation used inside text() block.")

        self.generic_visit(node)

def verify_ast(code: str) -> Tuple[bool, str]:
    """
    Verifies the generated AST using SecurityASTVisitor and Bandit SAST.
    Returns (passed, output).
    """
    passed = True
    output = ""

    # 1. Custom AST Visitor for deep security checks
    try:
        tree = ast.parse(code)
        visitor = SecurityASTVisitor()
        visitor.visit(tree)
        if visitor.errors:
            logger.warning("🛡️ [AST Verifier] Malicious code patterns detected!")
            return False, "SecurityASTVisitor errors:\n" + "\n".join(visitor.errors)
    except Exception as e:
        logger.error(f"🛡️ [AST Verifier] Failed to parse AST: {e}")
        return False, f"AST Parsing Error: {e}"

    # 2. Bandit SAST Scan
    try:
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name

        result = subprocess.run(
            ["bandit", "-r", temp_path, "-f", "txt"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            passed = False
            output = result.stdout + "\n" + result.stderr
            logger.warning("🛡️ [AST Verifier] Security vulnerability detected in generated code!")
            
    except FileNotFoundError:
        logger.warning("🛡️ [AST Verifier] Bandit is not installed. Skipping AST verification.")
    except Exception as e:
        logger.error(f"🛡️ [AST Verifier] Error running verification: {e}")
    finally:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

    return passed, output
