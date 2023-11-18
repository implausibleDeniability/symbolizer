from enum import auto, Enum


class UnaryOperationType(Enum):
    NEGATE = auto()
    SQRT = auto()


class BinaryOperationType(Enum):
    SUM = auto()
    MULT = auto()
    DIV = auto()

    def is_symmetric(self):
        if self in [self.SUM, self.MULT]:
            return True
        elif self in [self.DIV]:
            return False
        else:
            raise NotImplementedError("Symmetry undefined")

