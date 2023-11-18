import numpy as np

from symbolizer.operations import UnaryOperationType
from symbolizer.expression import InputVariable
from symbolizer.expression import UnaryExpression
from symbolizer.expression import BinaryExpression
from symbolizer.expression_hasher import ExpressionHasher


def test_expression_hasher_matches_double_negate():
    """Checks if 'x0' has the same hash as '--x0'"""
    expression = InputVariable(index=0)
    double_negate_expression = UnaryExpression(
        operation=UnaryOperationType.NEGATE,
        operand=UnaryExpression(
            operation=UnaryOperationType.NEGATE,
            operand=InputVariable(index=0),
        )
    )
    x = np.random.randn(5, 2)
    hasher = ExpressionHasher(x=x, tolerance=1e-6)

    assert hasher.hash(expression) == hasher.hash(double_negate_expression)
