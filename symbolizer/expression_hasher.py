import numpy as np

from symbolizer.compute_expression import compute_expression
from symbolizer.expression import Expression


class ExpressionHasher:
    def __init__(self, x, tolerance):
        self._x = x
        self._n_significant_digits = int(-np.log10(tolerance))

    def hash(self, expression: Expression) -> int:
        y = compute_expression(expression, self._x)
        y = np.round(y, self._n_significant_digits)
        return hash(y.data.tobytes())
