import logging

import numpy as np
from tqdm import tqdm

from symbolizer.operations import UnaryOperationType
from symbolizer.operations import BinaryOperationType
from symbolizer.expression import Expression
from symbolizer.expression import InputVariable
from symbolizer.expression import UnaryExpression
from symbolizer.expression import BinaryExpression
from symbolizer.expression import expression2str
from symbolizer.expression_iterator import ExpressionIterator
from symbolizer.compute_expression import compute_expression


class Symbolizer:
    def __init__(self, x, y, max_complexity: int = 3, tolerance: float = 1e-6):
        self.expression_iterator = ExpressionIterator(x, max_complexity, tolerance)
        self._tolerance = tolerance
        self.x = x
        self.y = y
        
    def run(self) -> str:
        """Given the set of pairs of variables and target variable
        gives approximate formula to compute y.
        """
        for expression in tqdm(self.expression_iterator):
            error = self._compute_expression_error(expression)
            if error < self._tolerance:
                return expression2str(expression)

    def _compute_expression_error(self, expression: Expression) -> float:
        values = compute_expression(expression, self.x)
        assert values.shape == self.y.shape
        error = ((self.y - values) ** 2).sum(axis=0)
        return error
