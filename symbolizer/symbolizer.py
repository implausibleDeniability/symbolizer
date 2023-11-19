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
from symbolizer.compute_expression_error import compute_expression_error
from symbolizer.constant_optimizer import ConstantOptimizer


class Symbolizer:
    def __init__(self, x, y, max_complexity: int = 3, tolerance: float = 1e-6, n_constants: int = 1):
        self._constant_optimizer = ConstantOptimizer(x, y, n_constants)
        self._expression_iterator = ExpressionIterator(x, y, self._constant_optimizer, max_complexity, tolerance)
        self._tolerance = tolerance
        self.x = x
        self.y = y
        
    def run(self) -> str:
        """Given the set of pairs of variables and target variable
        gives approximate formula to compute y.
        """
        for expression in tqdm(self._expression_iterator):
            constants = self._constant_optimizer.optimize(expression)
            logging.debug(f"For expression {expression2str(expression)} best found constants are {constants}")
            error = compute_expression_error(expression, self.x, self.y, constants)
            if error < self._tolerance:
                return expression2str(expression)
