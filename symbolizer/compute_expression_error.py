from symbolizer.expression import Expression
from symbolizer.compute_expression import compute_expression

def compute_expression_error(expression: Expression, x, y, constants=None) -> float:
    values = compute_expression(expression, x, constants)
    assert values.shape == y.shape, f"Shape mismatch: {values.shape} and {y.shape}"
    error = ((y - values) ** 2).sum(axis=0)
    return error
