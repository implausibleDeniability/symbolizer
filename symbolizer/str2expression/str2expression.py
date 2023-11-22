from symbolizer.expression import Expression
from .str_tokenizer import StrTokenizer
from .token_parser import TokenParser

def str2expression(string: str) -> Expression:
    tokens = StrTokenizer().tokenize(string)
    expression = TokenParser().tokens2expression(tokens)
    return expression
