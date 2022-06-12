"""Operations used in AcmeInstruments programs."""

import operator as builtin_operator
from dataclasses import dataclass


@dataclass
class Operation:
    value: int = 0


@dataclass
class Multiplication(Operation):
    value: int = 0
    operator = builtin_operator.mul


@dataclass
class Division(Operation):
    value: int = 0
    operator = builtin_operator.truediv


@dataclass
class Summation(Operation):
    value: int = 0
    operator = builtin_operator.add


def _set_value(_, a, b):
    return b


@dataclass
class SetInitialState(Operation):
    value: int = 0
    operator = _set_value
