import numpy as np

from symbolizer.operations import UnaryOperationType
from symbolizer.operations import BinaryOperationType
from symbolizer.expression import Expression
from symbolizer.expression import InputVariable
from symbolizer.expression import UnaryExpression
from symbolizer.expression import BinaryExpression


def compute_expression(expression: Expression, x: np.ndarray) -> np.ndarray: 
    if isinstance(expression, InputVariable):
        return x[:, expression.index]
    elif isinstance(expression, UnaryExpression):
        return _compute_unary_expression(expression, x)
    elif isinstance(expression, BinaryExpression):
        return _compute_binary_expression(expression, x)
    else:
        raise NotImplementedError("I dunno how to compute this expression")


def _compute_binary_expression(expression, x):
    if expression.operation == BinaryOperationType.SUM:
        return compute_expression(expression.left_operand, x) + compute_expression(expression.right_operand, x)
    elif expression.operation == BinaryOperationType.MULT:
        return compute_expression(expression.left_operand, x) * compute_expression(expression.right_operand, x)
    elif expression.operation == BinaryOperationType.DIV:
        return compute_expression(expression.left_operand, x) / compute_expression(expression.right_operand, x)
    else:
        raise NotImplementedError()


def _compute_unary_expression(expression, x):
    if expression.operation == UnaryOperationType.NEGATE:
        return -compute_expression(expression.operand, x)
    elif expression.operation == UnaryOperationType.SQRT:
        return np.sqrt(compute_expression(expression.operand, x))
    else:
        raise NotImplementedError()

