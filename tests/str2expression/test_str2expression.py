import numpy as np

from symbolizer import str2expression
from symbolizer.expression import *
from symbolizer.operations import *


def test_str2expression_simple_sum():
    actual_expression = str2expression('x0 + x1')
    expected_expression = BinaryExpression(
        operation=BinaryOperationType.SUM,
        left_operand=InputVariable(0),
        right_operand=InputVariable(1),
    )
    assert actual_expression == expected_expression


def test_str2expression_simple_diff():
    actual_expression = str2expression('x0 - x1')
    expected_expression = BinaryExpression(
        operation=BinaryOperationType.SUM,
        left_operand=InputVariable(0),
        right_operand=UnaryExpression(
            operation=UnaryOperationType.NEGATE,
            operand=InputVariable(1),
        )
    )
    assert actual_expression == expected_expression


def test_str2expression_parentheses():
    actual_expression = str2expression('x2 * (x0 + x1)')
    expected_expression = BinaryExpression(
        operation=BinaryOperationType.MULT,
        left_operand=InputVariable(2),
        right_operand=BinaryExpression(
            operation=BinaryOperationType.SUM,
            left_operand=InputVariable(0),
            right_operand=InputVariable(1),
        ),
    )
    assert actual_expression == expected_expression


def test_str2expression_sqrt():
    actual_expression = str2expression('sqrt(x0)')
    expected_expression = UnaryExpression(UnaryOperationType.SQRT, InputVariable(0))
    assert actual_expression == expected_expression


def test_str2expression_sqr():
    actual_expression = str2expression('sqr(x0)')
    expected_expression = UnaryExpression(UnaryOperationType.SQUARE, InputVariable(0))
    assert actual_expression == expected_expression


def test_str2expression_complex():
    actual_expression = str2expression('(sqr((x2 + x1) * x1) + sqrt(x1 + x0)) / (x0 / exp(x1))')

    sqr_expression = UnaryExpression(
        UnaryOperationType.SQUARE,
        BinaryExpression(
            BinaryOperationType.MULT,
            BinaryExpression(
                BinaryOperationType.SUM,
                InputVariable(2),
                InputVariable(1),
            ),
            InputVariable(1),
        ),
    )
    sqrt_expression = UnaryExpression(
        UnaryOperationType.SQRT,
        BinaryExpression(
            BinaryOperationType.SUM,
            InputVariable(1),
            InputVariable(0),
        )
    )
    denominator_expression = BinaryExpression(
        BinaryOperationType.DIV,
        InputVariable(0),
        UnaryExpression(
            UnaryOperationType.EXP,
            InputVariable(1),
        ),
    )
    expected_expression = BinaryExpression(
        BinaryOperationType.DIV,
        BinaryExpression(
            BinaryOperationType.SUM,
            sqr_expression,
            sqrt_expression,
        ),
        denominator_expression,
    )
    assert isinstance(actual_expression, BinaryExpression)
    assert actual_expression.right_operand == denominator_expression
    assert isinstance(actual_expression.left_operand, BinaryExpression)
    assert actual_expression.left_operand.left_operand == sqr_expression
    assert actual_expression.left_operand.right_operand == sqrt_expression
    assert actual_expression == expected_expression
