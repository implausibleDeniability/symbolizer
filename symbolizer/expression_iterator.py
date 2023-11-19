import logging

import numpy as np

from symbolizer.compute_expression import compute_expression
from symbolizer.expression import InputVariable
from symbolizer.expression import UnaryExpression
from symbolizer.expression import BinaryExpression
from symbolizer.expression import Constant
from symbolizer.expression import expression2str
from symbolizer.expression_hasher import ExpressionHasher
from symbolizer.operations import UnaryOperationType
from symbolizer.operations import BinaryOperationType


class ExpressionIterator:
    def __init__(self, x, y, constant_optimizer, max_complexity: int = 3, tolerance: float=1e-6):
        self._x = x
        self._y = y
        self._max_complexity = max_complexity
        self.expression_hasher = ExpressionHasher(x, tolerance, constant_optimizer)
        self._constant_optimizer = constant_optimizer

        self.expressions = []
        self.hashes = set()
        self._init_atomic_expressions()

    def _init_atomic_expressions(self):
        for i in range(self._x.shape[1]):
            atomic_expression = InputVariable(index=i)
            self.expressions.append(atomic_expression)
            self.hashes.add(self.expression_hasher.hash(atomic_expression))
        for i in range(self._constant_optimizer._n_constants):
            unknown_constant = Constant(i)
            self.expressions.append(unknown_constant)

    def __iter__(self):
        for idx, expression in enumerate(self.expressions):
            for new_expression in self._complexify_expression(expression, n_first_for_binary=idx):
                if new_expression.complexity > self._max_complexity: 
                    logging.debug(f"Skipping expression {expression2str(new_expression)}: complexity {new_expression.complexity} is too large")
                    continue
                constants = self._constant_optimizer.optimize(new_expression)
                if np.isnan(compute_expression(new_expression, self._x, constants)).any():
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
