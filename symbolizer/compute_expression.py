import numpy as np

from symbolizer.operations import UnaryOperationType
from symbolizer.operations import BinaryOperationType
from symbolizer.expression import Expression
from symbolizer.expression import InputVariable
from symbolizer.expression import UnaryExpression
from symbolizer.expression import BinaryExpression
from symbolizer.expression import Constant


def compute_expression(expression: Expression, x: np.ndarray, constants: np.ndarray) -> np.ndarray: 
    if isinstance(expression, InputVariable):
        return x[:, expression.index]
    if isinstance(expression, Constant):
        return constants[expression.index] * np.ones((x.shape[0]))
    elif isinstance(expression, UnaryExpression):
        return _compute_unary_expression(expression, x, constants)
    elif isinstance(expression, BinaryExpression):
        return _compute_binary_expression(expression, x, constants)
    else:
        raise NotImplementedError("I dunno how to compute this expression")


def _compute_binary_expression(expression, x, constants: np.ndarray):
    if expression.operation == BinaryOperationType.SUM:
        return compute_expression(expression.left_operand, x, constants) + compute_expression(expression.right_operand, x, constants)
    elif expression.operation == BinaryOperationType.MULT:
        return compute_expression(expression.left_operand, x, constants) * compute_expression(expression.right_operand, x, constants)
    elif expression.operation == BinaryOperationType.DIV:
        return compute_expression(expression.left_operand, x, constants) / compute_expression(expression.right_operand, x, constants)
    else:
        raise NotImplementedError()


def _compute_unary_expression(expression, x, constants: np.ndarray):
    if expression.operation == UnaryOperationType.NEGATE:
        return -compute_expression(expression.operand, x, constants)
    elif expression.operation == UnaryOperationType.SQRT:
        return np.sqrt(compute_expression(expression.operand, x, constants))
    elif expression.operation == UnaryOperationType.SQUARE:
        return compute_expression(expression.operand, x, constants) ** 2
    elif expression.operation == UnaryOperationType.EXP:
        return np.exp(compute_expression(expression.operand, x, constants))
    else:
        raise NotImplementedError()

