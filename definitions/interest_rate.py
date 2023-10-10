from decimal import Decimal
from enum import Enum
from functools import total_ordering
from typing import Optional


class Compounding(str, Enum):
    """
    Interest rates compounding conventions.
    """

    YEARLY = "Yearly"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"
    WEEKLY = "Weekly"
    DAILY = "Daily"
    CONTINUOUS = "Continuous"


@total_ordering
class InterestRate:
    """
    Definition of a nominal interest rate.
    By default, interest rates are considered to be on an annualized basis,
    i.e. with Compounding.YEARLY.
    """

    def __init__(self, rate: Decimal, compounding: Optional[Compounding] = Compounding.YEARLY) -> None:
        self.rate = rate
        self.compounding = compounding

    def __str__(self) -> str:
        return f"InterestRate(rate={self.rate}, compounding={self.compounding})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def annualized(self) -> Decimal:
        """
        Compoute annualized rate equivalent.
        """

        match self.compounding:
            case Compounding.YEARLY:
                return self.rate

            case Compounding.MONTHLY:
                return (1 + self.rate / 12) ** 12 - 1

            case Compounding.QUARTERLY:
                return (1 + self.rate / 4) ** 4 - 1

            case Compounding.WEEKLY:
                return (1 + self.rate / 52) ** 52 - 1

            case Compounding.DAILY:
                return (1 + self.rate / 365) ** 365 - 1

            case Compounding.CONTINUOUS:
                return Decimal.exp(self.rate) - 1

    def __eq__(self, other):
        if not isinstance(other, InterestRate):
            raise TypeError()

        return self.rate == other.rate and self.compounding == other.compounding

    def __lt__(self, other):
        if not isinstance(other, InterestRate):
            raise TypeError()

        return self.annualized < other.annualized
