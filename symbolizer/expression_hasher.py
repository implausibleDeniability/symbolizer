import numpy as np

from symbolizer.compute_expression import compute_expression
from symbolizer.expression import Expression


class ExpressionHasher:
    def __init__(self, x, tolerance, constant_optimizer):
        self._x = x
        self._n_significant_digits = int(-np.log10(tolerance))
        self._constant_optimizer = constant_optimizer

    def hash(self, expression: Expression) -> int:
        constants = self._constant_optimizer.optimize(expression)
        y = compute_expression(expression, self._x, constants)
        y = np.round(y, self._n_significant_digits)
        return hash(y.data.tobytes())
