import numpy as np

from symbolizer.expression import Expression
from symbolizer.compute_expression import compute_expression


def assert_expressions_equal_in_bounds(
    actual_expression: Expression, 
    expected_expression: Expression, 
    bounds: list[tuple[float, float]],
    n_points: int = 1000,
):
    bounds = np.array(bounds)
    x = np.random.uniform(low=bounds[:,0], high=bounds[:, 1], size=(n_points, len(bounds)))
    assert np.allclose(
        compute_expression(actual_expression, x),
        compute_expression(expected_expression, x),
        atol=1e-6,
    )
