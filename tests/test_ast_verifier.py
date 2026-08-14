import pytest
from ai_engine.ast_verifier import verify_python_syntax

def test_ast_verifier_valid():
    valid_code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
"""
    is_valid, err = verify_python_syntax(valid_code)
    assert is_valid is True
    assert err is None

def test_ast_verifier_invalid_syntax():
    invalid_code = """
def calculate_total(items)
    total = 0
"""
    is_valid, err = verify_python_syntax(invalid_code)
    assert is_valid is False
    assert "SyntaxError" in err
