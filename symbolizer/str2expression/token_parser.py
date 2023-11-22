from symbolizer.expression import *
from symbolizer.operations import BinaryOperationType
from symbolizer.operations import UnaryOperationType
from .str_tokenizer import ExpressionToken


class ParenthesesNotFoundError(Exception):
    pass


class TokenParser:
    def tokens2expression(self, tokens: list[ExpressionToken]) -> Expression:
        tokens = self._reduce_parentheses(tokens)
        self._reduce_unary_operations(tokens)
        self._reduce_mults_divs(tokens)
        self._reduce_sums(tokens)
        assert len(tokens) == 1, f"Expected only one token after all reductions, found {tokens}"
        return tokens[0]

    def _reduce_parentheses(
            self, 
            tokens: list[ExpressionToken],
        ) -> list[Expression | UnaryOperationType | BinaryOperationType]:
        """Computes everything in parentheses, and substitutes them with an expression"""
        while True:
            try:
                tokens = self._reduce_one_top_level_parentheses_pair(tokens)
            except ParenthesesNotFoundError:
                break
        return tokens

    def _reduce_one_top_level_parentheses_pair(
            self,
            tokens: list[ExpressionToken],
        ) -> list[ExpressionToken | UnaryExpression | BinaryExpression]:
        top_level_opening_parenthesis_index = None
        top_level_closing_parenthesis_index = None
        enclosure = 0
        for i, token in enumerate(tokens):
            if token == '(':
                if enclosure == 0:
                    top_level_opening_parenthesis_index = i
                enclosure += 1
            elif token == ')':
                enclosure -= 1
                if enclosure == 0:
                    top_level_closing_parenthesis_index = i
                    break
        if top_level_closing_parenthesis_index is None or top_level_closing_parenthesis_index is None:
            raise ParenthesesNotFoundError
        inner_expression = self.tokens2expression(tokens[top_level_opening_parenthesis_index + 1 : top_level_closing_parenthesis_index])
        reduced_tokens = tokens[:top_level_opening_parenthesis_index] + [inner_expression] + tokens[top_level_closing_parenthesis_index + 1:]
        return reduced_tokens

    def _reduce_unary_operations(
            self, 
            tokens: list[Expression | UnaryOperationType | BinaryOperationType],
        ) -> None:
        for i, token in enumerate(tokens):
            if type(token) == UnaryOperationType:
                assert isinstance(tokens[i+1], Expression)
                tokens[i] = UnaryExpression(
                        operation=token, 
                        operand=tokens.pop(i+1),
                    )

    def _reduce_mults_divs(
            self,
            tokens: list[Expression | BinaryOperationType],
        ) -> None:
        for i, token in enumerate(tokens):
            if (
                i + 1 < len(tokens) 
                and tokens[i + 1] in [BinaryOperationType.MULT, BinaryOperationType.DIV]
            ):
                assert isinstance(tokens[i], Expression), f"Expected Expression, found {tokens[i]}"
                assert isinstance(tokens[i+2], Expression), f"Expected Expression, found {tokens[i+2]}"
                tokens[i] = BinaryExpression(
                    right_operand=tokens.pop(i + 2),
                    operation=tokens.pop(i + 1), 
                    left_operand=tokens[i],
                )

    def _reduce_sums(
            self,
            tokens: list[Expression | BinaryOperationType],
        ) -> None:
        for i, token in enumerate(tokens):
            if i + 1 < len(tokens) and tokens[i + 1] == BinaryOperationType.SUM:
                tokens[i] = BinaryExpression(
                    right_operand=tokens.pop(i + 2),
                    operation=tokens.pop(i + 1), 
                    left_operand=tokens[i],
                )
