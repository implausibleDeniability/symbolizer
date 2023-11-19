import numpy as np
from scipy.optimize import minimize

from symbolizer.expression import Expression
from symbolizer.expression import expression2str
from symbolizer.compute_expression_error import compute_expression_error

class ConstantOptimizer:
    def __init__(self, x, y, n_constants):
        self._x = x
        self._y = y
        self._n_constants = n_constants
        self._computed_constants: dict[str, np.ndarray] = {}

    def optimize(self, expression) -> np.ndarray:
        if self._n_constants == 0: return np.array([])
        expression_str = expression2str(expression)
        if expression_str not in self._computed_constants:
            self._computed_constants[expression_str] = self._optimize(expression)
        return self._computed_constants[expression_str]

    def _optimize(self, expression: Expression):
        result = minimize(
            lambda constants: compute_expression_error(expression, self._x, self._y, constants),
            x0=np.zeros(self._n_constants),
            method='BFGS',
            options={
                "maxiter": 5000,
            }
        )
        constants = result.x
        return constants
