import numpy as np
import pytest
from scipy.stats import norm

from symbolizer import Symbolizer


def set_seed():
    np.random.seed(42)


def test_sum_of_two_variables():
    set_seed()
    x = np.random.randn(3, 2)
    y = x[:, 0] + x[:, 1]
    
    symbolizer = Symbolizer(x, y, n_constants=0)
    expression = symbolizer.run()

    assert expression == 'x0 + x1'


def test_product_of_two_variables():
    set_seed()
    x = np.random.randn(3, 2)
    y = x[:, 0] * x[:, 1]
    
    symbolizer = Symbolizer(x, y, n_constants=0)
    expression = symbolizer.run()

    assert expression == '(x0) * (x1)'


def test_division():
    set_seed()
    x = np.random.randn(3, 2)
    y = x[:, 0] / x[:, 1]
    
    symbolizer = Symbolizer(x, y, n_constants=0)
    expression = symbolizer.run()

    assert expression == '(x0) / (x1)'


def test_three_variables():
    set_seed()
    x = np.random.randn(5, 3)
    y = (x[:, 0] + x[:, 1]) * x[:, 2]

    symbolizer = Symbolizer(x, y, max_complexity=5)
    expression = symbolizer.run()

    assert expression == '(x2) * (x0 + x1)'


def test_four_variables():
    set_seed()
    x = np.random.randn(5, 4)
    y = (x[:, 0] + x[:, 1] * x[:, 2]) / (x[:, 0] + x[:, 3])

    symbolizer = Symbolizer(x, y, max_complexity=10, n_constants=0)
    expression = symbolizer.run()

    assert expression == '(x0 + (x1) * (x2)) / (x0 + x3)'


def test_with_constant():
    set_seed()
    x = np.random.randn(3, 1)
    const = 7.2
    y = const * x[:, 0]

    symbolizer = Symbolizer(x, y, max_complexity=10)
    expression = symbolizer.run()

    assert expression == '(x0) * (7.2)'


@pytest.mark.skip(reason='not fixed yet')
def test_std_gaussian_pdf():
    set_seed()
    x = np.random.randn(10, 1)
    y = norm.pdf(x[:, 0])

    symbolizer = Symbolizer(x, y, max_complexity=10, n_constants=2)
    expression = symbolizer.run()

    assert expression == '(C0) / (sqrt(exp((x0)^2)))'
