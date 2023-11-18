import numpy as np

from symbolizer import Symbolizer


def set_seed():
    np.random.seed(42)


def test_sum_of_two_variables():
    set_seed()
    x = np.random.randn(3, 2)
    y = x[:, 0] + x[:, 1]
    
    symbolizer = Symbolizer(x, y)
    expression = symbolizer.run()

    assert expression == 'x0 + x1'


def test_product_of_two_variables():
    set_seed()
    x = np.random.randn(3, 2)
    y = x[:, 0] * x[:, 1]
    
    symbolizer = Symbolizer(x, y)
    expression = symbolizer.run()

    assert expression == '(x0) * (x1)'


def test_division():
    set_seed()
    x = np.random.randn(3, 2)
    y = x[:, 0] / x[:, 1]
    
    symbolizer = Symbolizer(x, y)
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

    symbolizer = Symbolizer(x, y, max_complexity=10)
    expression = symbolizer.run()

    assert expression == '(x0 + (x1) * (x2)) / (x0 + x3)'
