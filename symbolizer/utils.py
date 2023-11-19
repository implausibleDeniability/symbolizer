import re
from typing import Literal

from symbolizer.expression import InputVariable
from symbolizer.expression import Constant
from symbolizer.operations import BinaryOperationType
from symbolizer.operations import UnaryOperationType

ExpressionToken = Literal['(', ')'] | InputVariable | Constant | BinaryOperationType | UnaryOperationType

def str2expression(string: str):
    tokens = _tokenize(string)

    operation_stack = []
    for token in tokens:
        if token == '(':
            operation_stack.append(token)
        elif token == ')':
            enclousre -= 1
        elif token.startswith('x'):
            operand = InputVariable(index=int(token[1:]))
        elif token == '+':
            pass

def _tokenize(string: str) -> list[ExpressionToken]:
    str_tokens: list[str] = _split_str_tokens(string)
    expression_tokens = _str_tokens2expression_tokens(str_tokens)
    return expression_tokens

def _split_str_tokens(string: str) -> list[str]:
    token_pattern = (
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
        r'|\^2'
    )
    tokens = re.findall(token_pattern, string)
    return tokens

def _str_tokens2expression_tokens(str_tokens: list[str]) -> list[ExpressionToken]:
    tokens = []
    for str_token in str_tokens:
        if str_token in '()':
            tokens.append(str_token)
        elif str_token == '+':
            tokens.append(BinaryOperationType.SUM)
        elif str_token == '*':
            tokens.append(BinaryOperationType.MULT)
        elif str_token == '/':
            tokens.append(BinaryOperationType.DIV)
        elif str_token == 'exp':
            tokens.append(UnaryOperationType.EXP)
        elif str_token == 'sqrt':
            tokens.append(UnaryOperationType.SQRT)
        elif str_token == '^2':
            tokens.append(UnaryOperationType.SQUARE)
        elif str_token == '-':
            if len(tokens) == 0 or tokens[-1] == '(' or tokens[-1] == '+':
                tokens.append(UnaryOperationType.NEGATE)
            else:
                tokens.extend([BinaryOperationType.SUM, UnaryOperationType.NEGATE])
        else:
            raise NotImplementedError()
    return tokens
