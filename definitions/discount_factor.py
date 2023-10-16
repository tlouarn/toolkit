from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from definitions.date import Date


# from definitions.interest_rate import InterestRate


@dataclass(frozen=True, eq=True)
class DiscountFactor:
    start: Date
    end: Date
    factor: Decimal

    @property
    def days(self) -> int:
        """
        :return: The number of calendar days between the start and end dates.
        """
        calendar_days = (self.end - self.start).days
        return calendar_days
