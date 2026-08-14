import sys
import subprocess
from logger import logger

def format_python_code(code_str: str) -> str:
    """
    Attempts to format Python code using 'black'.
    If black is not available or fails, returns the code stripped cleanly.
    """
    try:
        import black
        formatted_code = black.format_str(code_str, mode=black.FileMode())
        return formatted_code
    except Exception as e:
        logger.debug(f"Black formatting skipped: {e}")
        return code_str.strip() + "\n"
