import logging

import numpy as np

from symbolizer import Symbolizer


if __name__ == "__main__":
    logging.basicConfig(
        filename='debug.log', 
        format='%(levelname)s:%(message)s', 
        encoding='utf-8', 
        level=logging.DEBUG
    )
    x = np.array([0, 1, 2]).reshape(-1, 1)
    y = np.array([0, 2, 4])
    result = Symbolizer(x, y).run()
    print(result)

