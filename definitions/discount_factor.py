from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from definitions.date import Date
from definitions.interest_rate import Compounding, InterestRate


@dataclass(frozen=True, eq=True)
class DiscountFactor:
    start: Date
    end: Date
    factor: Decimal

    @classmethod
    def from_interest_rate(cls, start: Date, end: Date, interest_rate: InterestRate) -> DiscountFactor:
        interest = interest_rate.rate * (end - start).days / 360
        factor = 1 / (1 + interest)
        return cls(start=start, end=end, factor=factor)

    @property
    def days(self) -> int:
        """
        :return: The number of calendar days between the start and end dates.
        """
        calendar_days = (self.end - self.start).days
        return calendar_days

    def to_rate(self) -> InterestRate:
        """
        Convert the discount factor to a continuously compounded rate with ACT/360 day count.
        """
        rate = -Decimal.ln(self.factor) * Decimal(360) / max(Decimal(self.days), Decimal(1))
        return InterestRate(rate=rate, compounding=Compounding.CONTINUOUS)
