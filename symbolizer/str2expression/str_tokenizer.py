import re
from typing import Literal

from symbolizer.expression import *
from symbolizer.operations import BinaryOperationType
from symbolizer.operations import UnaryOperationType


ExpressionToken = Literal['(', ')'] | InputVariable | UnaryOperationType | BinaryOperationType 

class StrTokenizer:
    CONSTANT_PATTERN = r'|\d+\.?\d*' # https://stackoverflow.com/questions/12643009/regular-expression-for-floating-point-numbers
    POSSIBLE_TOKENS_PATTERN = (
        r'\('
        r'|\)'
        r'|x\d+'
        r'|C\d+'
        r'|\+'
        r'|\-'
        r'|\*'
        r'|\/'
        r'|sqrt'
        r'|exp'
        r'|sqr'
        + CONSTANT_PATTERN
    )

    def tokenize(self, string: str) -> list[ExpressionToken]:
        str_tokens: list[str] = self._split_str_tokens(string)
        expression_tokens = self._str_tokens2expression_tokens(str_tokens)
        return expression_tokens

    def _split_str_tokens(self, string: str) -> list[str]:
        tokens = re.findall(self.POSSIBLE_TOKENS_PATTERN, string)
        return tokens

    def _str_tokens2expression_tokens(self, str_tokens: list[str]) -> list[ExpressionToken]:
        tokens = []
        for str_token in str_tokens:
            if str_token in '()':
                tokens.append(str_token)
            elif str_token.startswith('x'):
                tokens.append(InputVariable(index=int(str_token[1:])))
            elif str_token.startswith('C'):
                tokens.append(UnknownConstant(index=int(str_token[1:])))
            elif re.fullmatch(self.CONSTANT_PATTERN, str_token):
                tokens.append(KnownConstant(float(str_token)))
            elif str_token == '+':
                tokens.append(BinaryOperationType.SUM)
            elif str_token == '-':
                if len(tokens) == 0 or tokens[-1] == '(' or tokens[-1] == '+':
                    tokens.append(UnaryOperationType.NEGATE)
                else:
                    tokens.extend([BinaryOperationType.SUM, UnaryOperationType.NEGATE])
            elif str_token == '*':
                tokens.append(BinaryOperationType.MULT)
            elif str_token == '/':
                tokens.append(BinaryOperationType.DIV)
            elif str_token == 'exp':
                tokens.append(UnaryOperationType.EXP)
            elif str_token == 'sqrt':
                tokens.append(UnaryOperationType.SQRT)
            elif str_token == 'sqr':
                tokens.append(UnaryOperationType.SQUARE)
            else:
                raise NotImplementedError(f"Unknown token {str_token}")
        return tokens
