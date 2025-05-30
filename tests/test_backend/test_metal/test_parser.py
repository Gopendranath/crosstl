import pytest
from typing import List
from crosstl.backend.Metal.MetalLexer import MetalLexer
from crosstl.backend.Metal.MetalParser import MetalParser


def tokenize_code(code: str) -> List:
    """Helper function to tokenize code."""
    lexer = MetalLexer(code)
    return lexer.tokenize()


def parse_code(tokens: List):
    """Test the parser
    Args:
        tokens (List): The list of tokens generated from the lexer

    Returns:
        ASTNode: The abstract syntax tree generated from the code
    """
    parser = MetalParser(tokens)
    return parser.parse()


def test_struct():
    code = """
    struct Vertex_INPUT {
    float3 position [[attribute(0)]];
    };

    struct Vertex_OUTPUT {
        float4 position [[position]];
        float2 vUV;
    };
    """
    try:
        tokens = tokenize_code(code)
        parse_code(tokens)
    except SyntaxError:
        pytest.fail("Struct parsing not implemented.")


def test_if():
    code = """
    float perlinNoise(float2 p) {
    if (p.x == p.y) {
        return 0.0;
    }
    return fract(sin(dot(p, float2(12.9898, 78.233))) * 43758.5453);
    }
    """
    try:
        tokens = tokenize_code(code)
        parse_code(tokens)
    except SyntaxError:
        pytest.fail("If statement parsing not implemented.")


def test_for():
    code = """
    float perlinNoise(float2 p) {
    for (int i = 0; i < 10; i = i + 1) {
        p.x += 0.1;
    }
    return fract(sin(dot(p, float2(12.9898, 78.233))) * 43758.5453);
    }
    """
    try:
        tokens = tokenize_code(code)
        parse_code(tokens)
    except SyntaxError:
        pytest.fail("For loop parsing not implemented.")


def test_else():
    code = """
    float perlinNoise(float2 p) {
    if (p.x == p.y) {
        return 0.0;
        }
    else {
        return fract(sin(dot(p, float2(12.9898, 78.233))) * 43758.5453);
        }
    }
    """
    try:
        tokens = tokenize_code(code)
        parse_code(tokens)
    except SyntaxError:
        pytest.fail("Else statement parsing not implemented.")


def test_function_call():
    code = """
    #include <metal_stdlib>
    using namespace metal;

    float perlinNoise(float2 p) {
        return fract(sin(dot(p, float2(12.9898, 78.233))) * 43758.5453);
    }


    struct Fragment_INPUT {
        float2 vUV [[stage_in]];
    };

    struct Fragment_OUTPUT {
        float4 fragColor [[color(0)]];
    };

    fragment Fragment_OUTPUT fragment_main(Fragment_INPUT input [[stage_in]]) {
        Fragment_OUTPUT output;
        float noise = perlinNoise(input.vUV);
        float height = noise * 10.0;
        float3 color = float3(height / 10.0, 1.0 - height / 10.0, 0.0);
        output.fragColor = float4(color, 1.0);
        return output;
    }
    """
    try:
        tokens = tokenize_code(code)
        parse_code(tokens)
    except SyntaxError:
        pytest.fail("Function call parsing not implemented.")


def test_if_else():
    code = """
    float perlinNoise(float2 p) {
        if (p.x == p.y) {
            return 0.0;
        }
        if (p.x > p.y) {
            return 1.0;
        }
        else if (p.x > p.y) {
            return 1.0;
        }

        else if (p.x < p.y) {
            return -1.0;
        }

        else {
            return fract(sin(dot(p, float2(12.9898, 78.233))) * 43758.5453);
        }
    }
    """
    try:
        tokens = tokenize_code(code)
        parse_code(tokens)
    except SyntaxError:
        pytest.fail("If-else statement parsing not implemented.")


def test_mod_parsing():
    code = """
    fragment float4 fragmentMain() {
        int a = 10 % 3;  // Basic modulus
        return float4(1.0);
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


def test_const_declarations():
    code = """
    void main() {
        const float PI = 3.14159;
        const int VERSION = 100;
        float radius = 5.0;
        float area = PI * radius * radius;
    }
    """
    try:
        tokens = tokenize_code(code)
        parse_code(tokens)
    except SyntaxError as e:
        pytest.fail(f"Const variable declaration parsing not implemented: {e}")


if __name__ == "__main__":
    pytest.main()
