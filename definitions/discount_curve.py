from __future__ import annotations

from enum import Enum

from definitions.date import Date
from definitions.discount_factor import DiscountFactor

"""
Ways to instantiate a DiscountFactor:

From two cash-flows:
df = DiscountFactor.from_cashflows(cash_flow, cash_flow2)
df = DiscountFactor.from_interest_rate(interest_rate, start, end)



"""


class Interpolation(str, Enum):
    FLAT_FORWARD = "FlatForward"


class DiscountCurve:
    def __init__(self, discount_factors: list[DiscountFactor], interpolation: Interpolation):
        self.discount_factors = discount_factors
        self.interpolation = interpolation

    def add(self, discount_factor: DiscountFactor) -> None:
        self.discount_factors.append(discount_factor)

    def compute_discount_factor(self, start: Date, end: Date) -> DiscountFactor:
        # Interpolate using a preferred method CONSTANT_FORWARD_RATES
        pass

    def get(self, date: Date) -> DiscountFactor:


    def interpolate(self, start: Date, end: Date) -> DiscountFactor:
        pass