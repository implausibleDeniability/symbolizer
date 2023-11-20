from dataclasses import dataclass
from functools import cached_property

from symbolizer.operations import BinaryOperationType
from symbolizer.operations import UnaryOperationType


@dataclass(frozen=True)
class Expression:
    @cached_property
    def complexity(self) -> int:
        raise NotImplementedError()


@dataclass(frozen=True)
class BinaryExpression(Expression):
    operation: BinaryOperationType
    left_operand: Expression
    right_operand: Expression

    @cached_property
    def complexity(self) -> int:
        return self.left_operand.complexity + self.right_operand.complexity + 1


@dataclass(frozen=True)
class UnaryExpression(Expression):
    operation: UnaryOperationType
    operand: Expression

    @cached_property
    def complexity(self) -> int:
        return self.operand.complexity + 1


@dataclass(frozen=True)
class InputVariable(Expression):
    index: int

    @property
    def complexity(self) -> int:
        return 1


@dataclass(frozen=True)
class UnknownConstant(Expression):
    index: int

    @property
    def complexity(self) -> int:
        return 1


@dataclass(frozen=True)
class KnownConstant(Expression):
    value: float

    @property
    def complexity(self) -> int:
        return 1
    

def expression2str(expression: Expression) -> str:
    if isinstance(expression, InputVariable):
        return f"x{expression.index}"
    elif isinstance(expression, UnknownConstant):
        return f"C{expression.index}"
    elif isinstance(expression, KnownConstant):
        return str(round(expression.value, 6))
    elif expression.operation == UnaryOperationType.NEGATE:
        return "-" + expression2str(expression.operand)
    elif expression.operation == UnaryOperationType.SQRT:
        return "sqrt(" + expression2str(expression.operand) + ")"
    elif expression.operation == UnaryOperationType.SQUARE:
        return "(" + expression2str(expression.operand) + ")^2"
    elif expression.operation == UnaryOperationType.EXP:
        return "exp(" + expression2str(expression.operand) + ")"
    elif expression.operation == BinaryOperationType.SUM:
        return f"{expression2str(expression.left_operand)} + {expression2str(expression.right_operand)}"
    elif expression.operation == BinaryOperationType.MULT:
        return f"({expression2str(expression.left_operand)}) * ({expression2str(expression.right_operand)})"
    elif expression.operation == BinaryOperationType.DIV:
        return f"({expression2str(expression.left_operand)}) / ({expression2str(expression.right_operand)})"
    else:
        raise NotImplementedError()


