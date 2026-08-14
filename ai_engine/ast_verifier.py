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
