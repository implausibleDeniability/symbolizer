import logging

import numpy as np

from symbolizer.compute_expression import compute_expression
from symbolizer.expression import InputVariable
from symbolizer.expression import UnaryExpression
from symbolizer.expression import BinaryExpression
from symbolizer.expression import UnknownConstant
from symbolizer.expression import expression2str
from symbolizer.expression_iterator.expression_hasher import ExpressionHasher
from symbolizer.operations import UnaryOperationType
from symbolizer.operations import BinaryOperationType
from symbolizer.expression_iterator.complexity_ordered_set import ComplexityOrderedSet


class ExpressionIterator:
    def __init__(self, x, y, constant_optimizer, max_complexity: int = 3, tolerance: float=1e-6):
        self._x = x
        self._y = y
        self._max_complexity = max_complexity
        self.expression_hasher = ExpressionHasher(x, tolerance)
        self._constant_optimizer = constant_optimizer

        self.expressions_processed = []
        self.expressions_to_process = ComplexityOrderedSet()
        self._hashes = set()
        self._init_atomic_expressions()

    def _init_atomic_expressions(self):
        for i in range(self._x.shape[1]):
            atomic_expression = InputVariable(index=i)
            self.expressions_to_process.add(atomic_expression)
        for i in range(self._constant_optimizer._n_constants):
            unknown_constant = UnknownConstant(i)
            self.expressions_to_process.add(unknown_constant)

    def __iter__(self):
        while len(self.expressions_to_process) > 0:
            expression = self.expressions_to_process.pop_min()
            optimized_expression = self._constant_optimizer.optimize(expression)
            if self._check_expression_returns_nan(optimized_expression): continue
            if self._check_expression_is_duplicate(optimized_expression): continue
            self.expressions_processed.append(expression)
            self._hashes.add(self.expression_hasher.hash(optimized_expression))
            for new_expression in self._complexify_expression(expression):
                if self._check_expression_is_too_complex(new_expression): continue
                self.expressions_to_process.add(new_expression)
            logging.debug(f"New expression: {expression2str(expression)}, complexity={expression.complexity}")
            yield optimized_expression

    def _complexify_expression(self, expression):
        # try unary
        for operation in UnaryOperationType:
            yield UnaryExpression(operation, expression)
        # try binary
        for operation in BinaryOperationType:
            for other_expression in self.expressions_processed:
                yield BinaryExpression(operation, other_expression, expression)
                if not operation.is_symmetric():
                    yield BinaryExpression(operation, expression, other_expression)

    def _check_expression_is_too_complex(self, expression):
        if expression.complexity > self._max_complexity: 
            logging.debug(f"Skipping expression {expression2str(expression)}: complexity {expression.complexity} is too large")
            return True
        return False

    def _check_expression_returns_nan(self, expression):
        if np.isnan(compute_expression(expression, self._x)).any():
            logging.debug(f"Skipping expression {expression2str(expression)}: NaN")
            return True
        return False

    def _check_expression_is_duplicate(self, expression):
        if self.expression_hasher.hash(expression) in self._hashes:
            logging.debug(f"Skipping expression {expression2str(expression)}: hash exists")
            return True
        return False
