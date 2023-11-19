from symbolizer.utils import _split_str_tokens

def test_tokenize():
    str_expression = "(sqrt((x0) * (C0))) / (exp((C1 + x1)^2)"
    expected_tokens = ["(", "sqrt", "(", "(", "x0", ")", "*", "(", "C0", ")", ")", ")", "/", "(", "exp", "(", "(", "C1", "+", "x1", ")", "^2", ")"]
    assert _split_str_tokens(str_expression) == expected_tokens
