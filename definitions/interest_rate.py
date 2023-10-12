from decimal import Decimal
from enum import Enum
from functools import total_ordering
from typing import Optional

from definitions.compound_factor import CompoundFactor
from definitions.date import Date
from definitions.day_count import DayCountConvention
from definitions.discount_factor import DiscountFactor


class CompoundingFrequency(str, Enum):
    """
    Interest rates compounding frequencies.
    """

    YEARLY = "Yearly"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"
    WEEKLY = "Weekly"
    DAILY = "Daily"
    CONTINUOUS = "Continuous"


class SimpleInterestRate:
    def __init__(self):
        rate: Decimal
        convention: DayCountConvention


class CompoundInterestRate:
    def __init__(self):
        rate: Decimal
        convention: DayCountConvention
        compounding: CompoundingFrequency


@total_ordering
class InterestRate:
    def __init__(
        self,
        rate: Decimal,
        convention: Optional[DayCountConvention] = DayCountConvention.ACTUAL_360,
        compounding: Optional[CompoundingFrequency] = CompoundingFrequency.YEARLY,
    ) -> None:
        """
        Main constructor of the InterestRate object.
        A nominal interest rate expressed per annum cannot be defined without an associated
        day count convention (ACT/360, 30E/360 etc.) and a compounding frequency.
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
            case CompoundingFrequency.YEARLY:
                return self.rate

            case CompoundingFrequency.MONTHLY:
                return (1 + self.rate / 12) ** 12 - 1

            case CompoundingFrequency.QUARTERLY:
                return (1 + self.rate / 4) ** 4 - 1

            case CompoundingFrequency.WEEKLY:
                return (1 + self.rate / 52) ** 52 - 1

            case CompoundingFrequency.DAILY:
                return (1 + self.rate / 365) ** 365 - 1

            case CompoundingFrequency.CONTINUOUS:
                return Decimal.exp(self.rate) - 1

    def __eq__(self, other):
        if not isinstance(other, InterestRate):
            raise TypeError()

        return self.rate == other.rate and self.convention == other.convention and self.compounding == other.compounding

    def __lt__(self, other):
        if not isinstance(other, InterestRate):
            raise TypeError()

        return self.effective < other.effective

    def to_compound_factor(self, start: Date, end: Date) -> CompoundFactor:
        """
        Convert a nominal interest rate to a discount factor between two dates.
        :param start: start date
        :param end: end date
        :return: the corresponding compound factor
        """

        pass

    def to_discount_factor(self, start: Date, end: Date) -> DiscountFactor:
        pass
