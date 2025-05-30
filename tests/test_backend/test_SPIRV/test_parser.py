import pytest
from typing import List
from crosstl.backend.SPIRV.VulkanLexer import VulkanLexer
from crosstl.backend.SPIRV import VulkanParser


def parse_code(tokens: List):
    """Test the parser
    Args:
        tokens (List): The list of tokens generated from the lexer

    Returns:
        ASTNode: The abstract syntax tree generated from the code
    """
    parser = VulkanParser(tokens)
    return parser.parse()


def tokenize_code(code: str) -> List:
    """Helper function to tokenize code."""
    lexer = VulkanLexer(code)
    return lexer.tokenize()


def test_mod_parsing():
    code = """
    
    void main() {
        int a = 10 % 3;  // Basic modulus
    }
    """
    try:
        tokens = tokenize_code(code)
        parse_code(tokens)
    except SyntaxError:
        pytest.fail("Modulus operator parsing not implemented")


def test_bitwise_not_parsing():
    code = """
    void main() {
        int a = 5;
        int b = ~a;  // Bitwise NOT
    }
    """
    try:
        tokens = tokenize_code(code)
        parse_code(tokens)
    except SyntaxError:
        pytest.fail("Bitwise NOT operator parsing not implemented")


if __name__ == "__main__":
    pytest.main()
