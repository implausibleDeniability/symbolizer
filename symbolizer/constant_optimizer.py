import numpy as np
from scipy.optimize import minimize, shgo

from symbolizer.expression import Expression
from symbolizer.expression import InputVariable
from symbolizer.expression import UnaryExpression
from symbolizer.expression import BinaryExpression
from symbolizer.expression import UnknownConstant
from symbolizer.expression import KnownConstant
from symbolizer.expression import expression2str
from symbolizer.compute_expression_error import compute_expression_error

class ConstantOptimizer:
    MAX_ERROR = 1e5

    def __init__(self, x, y, n_constants):
        self._x = x
        self._y = y
        self._n_constants = n_constants
        self._computed_constants: dict[str, np.ndarray] = {}

    def optimize(self, expression: Expression) -> np.ndarray:
        if self._n_constants == 0: return expression
        expression_str = expression2str(expression)
        if expression_str not in self._computed_constants:
            self._computed_constants[expression_str] = self._optimize(expression)
        return self._computed_constants[expression_str]

    def _optimize(self, expression: Expression) -> Expression:
        constants = self._find_constants(expression)
        optimized_expression = self._substitute_constants(expression, constants)
        return optimized_expression

    def _find_constants(self, expression: Expression) -> np.ndarray:
        def error_function(constants):
            error = compute_expression_error(expression, self._x, self._y, constants)
            if np.isnan(error) or error > self.MAX_ERROR:
                error = self.MAX_ERROR
            return error 

        result = shgo(error_function, bounds=[(-10, 10),]*self._n_constants)
        constants = result.x
        return constants

    def _substitute_constants(self, expression: Expression, constants: np.ndarray) -> Expression:
        if isinstance(expression, UnaryExpression):
            return UnaryExpression(
                expression.operation, 
                self._substitute_constants(expression.operand, constants),
            )
        elif isinstance(expression, BinaryExpression):
            return BinaryExpression(
                expression.operation, 
                self._substitute_constants(expression.left_operand, constants),
                self._substitute_constants(expression.right_operand, constants),
            )
        elif isinstance(expression, UnknownConstant):
            return KnownConstant(value=constants[expression.index])
        elif type(expression) in [InputVariable, KnownConstant]:
            return expression
        else:
            raise NotImplementedError()
