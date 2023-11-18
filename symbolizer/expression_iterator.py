from symbolizer.operations import UnaryOperationType
from symbolizer.operations import BinaryOperationType
from symbolizer.expression import InputVariable
from symbolizer.expression import UnaryExpression
from symbolizer.expression import BinaryExpression


class ExpressionIterator:
    def __init__(self, n_input_variables: int, max_complexity: int = 3):
        self._n_input_variables = n_input_variables
        self._max_complexity = max_complexity
        self.expressions = []
        self._init_atomic_expressions()

    def _init_atomic_expressions(self):
        self.expressions += [
            InputVariable(index=i)
            for i in range(self._n_input_variables)
        ]

    def __iter__(self):
        for expression in self.expressions:
            for new_expression in self._complexify_expression(expression):
                if new_expression.complexity <= self._max_complexity:
                    self.expressions.append(new_expression)
                    yield new_expression

    def _complexify_expression(self, expression):
        # try unary
        for operation in UnaryOperationType:
            yield UnaryExpression(operation, expression)
        # try binary
        for operation in BinaryOperationType:
            for other_expression in self.expressions:
                yield BinaryExpression(operation, expression, other_expression)
                if not operation.is_symmetric():
                    yield BinaryExpression(operation, other_expression, expression)

