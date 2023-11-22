from symbolizer.str2expression.str_tokenizer import StrTokenizer

def test_tokenizer_splits_correctly():
    str_expression = "(sqrt((x0) * (C0))) / (exp(sqr(C1 + x1))"
    tokenizer = StrTokenizer()
    expected_tokens = ["(", "sqrt", "(", "(", "x0", ")", "*", "(", "C0", ")", ")", ")", "/", "(", "exp", "(", "sqr", "(", "C1", "+", "x1", ")", ")"]
    assert tokenizer._split_str_tokens(str_expression) == expected_tokens
