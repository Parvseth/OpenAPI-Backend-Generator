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

def verify_ast(code: str) -> Tuple[bool, str]:
    """
    Verifies the generated AST using Bandit SAST before returning it to the engine.
    Writes the code to a temporary file, scans it, and returns (passed, output).
    """
    passed = True
    output = ""
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
