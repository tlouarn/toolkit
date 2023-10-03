from dataclasses import dataclass
from datetime import date
from typing import Literal


@dataclass
class Option:
    """
    An Option is defined by its type, its strike and its maturity.
    """

    type: Literal["CALL", "PUT"]
    strike: float
    maturity: date


@dataclass
class Call:
    strike: float
    maturity: date


@dataclass
class Put:
    strike: float
    maturity: date


# Option = Call | Put
option = Call(strike=100.0, maturity=date(2023, 12, 15))
