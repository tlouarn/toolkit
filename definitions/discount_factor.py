from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from definitions.date import Date
from definitions.interest_rate import InterestRate
from instruments.deposit import Deposit


@dataclass
class DiscountFactor:
    start: Date
    end: Date
    factor: Decimal

    @classmethod
    def from_interest_rate(cls, start: Date, end: Date, interest_rate: InterestRate) -> DiscountFactor:
        interest = interest_rate.rate * (end - start).days / 360
        factor = 1 / (1 + interest)
        return cls(start=start, end=end, factor=factor)
