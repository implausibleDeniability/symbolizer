from collections import defaultdict

from symbolizer.expression import Expression


class ComplexityOrderedSet:
    def __init__(self):
        self.complexity2expression: dict[int, Expression] = defaultdict(lambda: [])
        self.current_min_complexity = 1
        self.element_counter = 0

    def __len__(self):
        return self.element_counter

    def add(self, expression: Expression) -> None:
        self.complexity2expression[expression.complexity].append(expression)
        self.element_counter += 1

    def pop_min(self) -> Expression:
        assert self.element_counter > 0
        if len(self.complexity2expression[self.current_min_complexity]) > 0:
            return self.complexity2expression[self.current_min_complexity].pop(0)
            self.element_counter -= 1
        else:
            self.current_min_complexity += 1
            return self.pop_min()
