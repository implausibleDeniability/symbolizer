from dataclasses import dataclass
from functools import cached_property

from symbolizer.operations import BinaryOperationType
from symbolizer.operations import UnaryOperationType


@dataclass
class Expression:
    @cached_property
    def complexity(self) -> int:
        raise NotImplementedError()


@dataclass
class BinaryExpression(Expression):
    operation: BinaryOperationType
    left_operand: Expression
    right_operand: Expression

    @cached_property
    def complexity(self) -> int:
        return self.left_operand.complexity + self.right_operand.complexity + 1


@dataclass
class UnaryExpression(Expression):
    operation: UnaryOperationType
    operand: Expression

    @cached_property
    def complexity(self) -> int:
        return self.operand.complexity + 1


@dataclass
class InputVariable(Expression):
    index: int

    @property
    def complexity(self) -> int:
        return 1


@dataclass
class Constant(Expression):
    index: int

    @property
    def complexity(self) -> int:
        return 1
    

def expression2str(expression: Expression) -> str:
    if isinstance(expression, InputVariable):
        return f"x{expression.index}"
    if isinstance(expression, Constant):
        return f"C{expression.index}"
    elif expression.operation == UnaryOperationType.NEGATE:
        return "-" + expression2str(expression.operand)
    elif expression.operation == UnaryOperationType.SQRT:
        return "sqrt(" + expression2str(expression.operand) + ")"
    elif expression.operation == BinaryOperationType.SUM:
        return f"{expression2str(expression.left_operand)} + {expression2str(expression.right_operand)}"
    elif expression.operation == BinaryOperationType.MULT:
        return f"({expression2str(expression.left_operand)}) * ({expression2str(expression.right_operand)})"
    elif expression.operation == BinaryOperationType.DIV:
        return f"({expression2str(expression.left_operand)}) / ({expression2str(expression.right_operand)})"
    else:
        raise NotImplementedError()


