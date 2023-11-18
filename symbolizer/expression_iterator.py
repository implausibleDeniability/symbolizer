import logging

import numpy as np

from symbolizer.compute_expression import compute_expression
from symbolizer.expression import InputVariable
from symbolizer.expression import UnaryExpression
from symbolizer.expression import BinaryExpression
from symbolizer.expression import expression2str
from symbolizer.expression_hasher import ExpressionHasher
from symbolizer.operations import UnaryOperationType
from symbolizer.operations import BinaryOperationType


class ExpressionIterator:
    def __init__(self, x, max_complexity: int = 3, tolerance=1e-6):
        self._x = x
        self._n_input_variables = x.shape[1]
        self._max_complexity = max_complexity
        self.expressions = []
        self.expression_hasher = ExpressionHasher(x, tolerance)
        self.hashes = set()
        self._init_atomic_expressions()

    def _init_atomic_expressions(self):
        for i in range(self._n_input_variables):
            atomic_expression = InputVariable(index=i)
            self.expressions.append(atomic_expression)
            self.hashes.add(self.expression_hasher.hash(atomic_expression))

    def __iter__(self):
        for idx, expression in enumerate(self.expressions):
            for new_expression in self._complexify_expression(expression, n_first_for_binary=idx):
                if new_expression.complexity > self._max_complexity: 
                    logging.debug(f"Skipping expression {expression2str(new_expression)}: complexity {new_expression.complexity} is too large")
                    continue
                if np.isnan(compute_expression(new_expression, self._x)).any():
                    logging.debug(f"Skipping expression {expression2str(new_expression)}: NaN")
                    continue
                if self.expression_hasher.hash(new_expression) in self.hashes:
                    logging.debug(f"Skipping expression {expression2str(new_expression)}: hash exists")
                    continue
                self.expressions.append(new_expression)
                self.hashes.add(self.expression_hasher.hash(new_expression))
                logging.debug(f"New expression: {expression2str(new_expression)}, complexity={new_expression.complexity}")
                yield new_expression

    def _complexify_expression(self, expression, n_first_for_binary):
        # try unary
        for operation in UnaryOperationType:
            yield UnaryExpression(operation, expression)
        # try binary
        for operation in BinaryOperationType:
            for other_expression in self.expressions[:n_first_for_binary]:
                yield BinaryExpression(operation, other_expression, expression)
                if not operation.is_symmetric():
                    yield BinaryExpression(operation, expression, other_expression)

