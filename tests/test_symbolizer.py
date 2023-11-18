import numpy as np

from symbolizer import Symbolizer


def set_seed():
    np.random.seed(42)


def test_sum_of_two_variables():
    x = np.random.randn(3, 2)
    y = x[:, 0] + x[:, 1]
    
    symbolizer = Symbolizer(x, y)
    expression = symbolizer.run()

    assert expression == 'x0 + x1'

