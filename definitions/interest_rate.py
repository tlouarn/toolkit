from decimal import Decimal
from functools import total_ordering
from typing import Optional

from definitions.day_count import DayCountConvention
from definitions.frequency import Frequency


class SimpleInterestRate:
    def __init__(self):
        rate: Decimal
        convention: DayCountConvention


class CompoundInterestRate:
    def __init__(self):
        rate: Decimal
        convention: DayCountConvention
        compounding: Frequency


@total_ordering
class InterestRate:
    def __init__(
        self,
        rate: Decimal,
        convention: Optional[DayCountConvention] = DayCountConvention.ACTUAL_360,
        compounding: Optional[Frequency] = Frequency.ANNUAL,
    ) -> None:
        """
        Main constructor of the InterestRate object.
        A nominal interest rate expressed per annum cannot be defined without an associated
        day count convention (ACT/360, 30E/360 etc.) and a compounding frequency (MONTHLY, ANNUAL).
        """
        self.rate = rate
        self.convention = convention
        self.compounding = compounding

    def __str__(self) -> str:
        return f"InterestRate(rate={self.rate}, convention={self.convention}, compounding={self.compounding})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def effective(self) -> Decimal:
        """
        Compoute effective rate equivalent.
        """

        match self.compounding:
            case Frequency.ANNUAL:
                return self.rate

            case Frequency.MONTHLY:
                return (1 + self.rate / 12) ** 12 - 1

            case Frequency.QUARTERLY:
                return (1 + self.rate / 4) ** 4 - 1

            case Frequency.WEEKLY:
                return (1 + self.rate / 52) ** 52 - 1

            case Frequency.DAILY:
                return (1 + self.rate / 365) ** 365 - 1

            case Frequency.CONTINUOUS:
                return Decimal.exp(self.rate) - 1

    def __eq__(self, other):
        if not isinstance(other, InterestRate):
            raise TypeError()

        return self.rate == other.rate and self.convention == other.convention and self.compounding == other.compounding

    def __lt__(self, other):
        if not isinstance(other, InterestRate):
            raise TypeError()

        return self.effective < other.effective
