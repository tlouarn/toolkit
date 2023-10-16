from decimal import Decimal
from functools import total_ordering
from typing import Optional

from definitions.date import Date
from definitions.day_count import DayCountConvention, compute_year_fraction
from definitions.frequency import Frequency

# TODO better modeling of interest rates
"""
class AbstractInterestRate(ABC):

    @abstractmethod
    def to_discount_factor() -> Decimal:
    
    
class SimpleInterestRate:


class ContinuousInterestRate:


class CompoundedInterestRate:


Factory function:

def interest_rate(rate: Decimal, day_count: DayCountConvention, type: Simple | Continuous | Compounded, freq: )
    if simple:
        return SimpleInterestRate(rate, day_count)
        return ContinuousInterestRate(rate, day_count)
        return CompoundedInterestRate(rate, day_count, frequency)


rate = interest_rate(Decimal("0.01"), DayCount("ModifiedFollowing"), Compounding("Simple"))
rate = interest_rate(Decimal("0.01"), DayCount("ModifiedFollowing"), Compounding("Continuous"))
rate = interest_rate(Decimal("0.01"), DayCount("ModifiedFollowing"), Compounding("Compounded"), Frequency("Monthly"))

Compounding = Simple | Continuous | Annual | Quarterly | Monthly | Weekly | Daily

"""


# NO_COMPOUNDING, DISCRETE COMPOUNDING or CONTINUOUS COMPOUNDING


@total_ordering
class InterestRate:
    def __init__(
        self,
        rate: Decimal,
        day_count: Optional[DayCountConvention] = DayCountConvention.ACTUAL_360,
        compounding: Optional[Frequency] = Frequency.ANNUAL,
    ) -> None:
        """
        A nominal interest rate expressed per annum cannot be defined
        without an associated day count convention (ACT/360, 30E/360, etc.)
        and a compounding frequency (MONTHLY, ANNUAL, etc.).
        """
        self.rate = rate
        self.day_count = day_count
        self.compounding = compounding

    def __str__(self) -> str:
        return f"InterestRate(rate={self.rate}, day_count={self.day_count}, compounding={self.compounding})"

    def __repr__(self) -> str:
        return str(self)

    def to_discount_factor(self, start: Date, end: Date) -> Decimal:
        """
        Compute the discount factor between two dates.
        Note: we need to provide actual dates, and not simply a number of days, in order
        to properly apply the day count convention and compute the time in years.

        :param start: start date
        :param end: end date
        :return: the discount factor
        """
        compound_factor = self.to_compound_factor(start=start, end=end)
        factor = 1 / compound_factor
        return factor

    def to_compound_factor(self, start: Date, end: Date) -> Decimal:
        """
        Compute the compound factor between two dates.
        Note: we need to provide actual dates, and not simply a number of days, in order
        to properly apply the day count convention and compute the time in years.

        :param start: start date
        :param end: end date
        :return: the compound factor
        """
        t = compute_year_fraction(start=start, end=end, day_count=self.day_count)

        match self.compounding:
            case Frequency.NONE:
                factor = 1 + self.rate * t

            case Frequency.ANNUAL:
                factor = (1 + self.rate) ** t

            case Frequency.SEMI_ANNUAL:
                factor = (1 + self.rate / 2) ** (t * 2)

            case Frequency.QUARTERLY:
                factor = (1 + self.rate / 4) ** (t * 4)

            case Frequency.MONTHLY:
                factor = (1 + self.rate / 12) ** (t * 12)

            case Frequency.CONTINUOUS:
                factor = Decimal.exp(self.rate * t)

            case _:
                raise NotImplementedError()

        return factor

    @property
    def effective(self) -> Decimal:
        """
        Compute effective annual rate equivalent.
        """

        match self.compounding:
            case Frequency.ANNUAL:
                return self.rate

            case Frequency.SEMI_ANNUAL:
                return InterestRate(1 + self.rate / InterestRate(2)) ** InterestRate(2) - 1

            case Frequency.MONTHLY:
                return InterestRate(1 + self.rate / InterestRate(12)) ** InterestRate(12) - 1

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

        return self.rate == other.rate and self.day_count == other.day_count and self.compounding == other.compounding

    def __lt__(self, other):
        if not isinstance(other, InterestRate):
            raise TypeError()

        return self.effective < other.effective
