from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from definitions import Date, DayCount
from instruments.deposit import FixedRateDeposit

"""
Ways to instantiate a DiscountFactor:

From two cash-flows:
df = DiscountFactor.from_cashflows(cash_flow, cash_flow2)
df = DiscountFactor.from_interest_rate(interest_rate, start, end)



"""



@dataclass
class DiscountFactor:
    start: Date
    end: Date
    value: float

    @classmethod
    def from_interest_rate(cls, interest_rate: InterestRate, start: dt.date, end: dt.date):
        days = (end - start).days
        day_count =

    @classmethod
    def from_deposit(cls, deposit: FixedRateDeposit) -> DiscountFactor:
        """
        Instantiate a DiscountFactor from a FixedRateDeposit.
        :param deposit: FixedRateDeposit
        :return: DiscountFactor
        """
        days = (deposit.end - deposit.start).days
        convention = 360 if deposit.convention == DayCount.ACT_360 else 365
        df = 1 / (1 + deposit.rate * days / convention)
        return DiscountFactor(date=deposit.end, value=df)


class DiscountCurve:
    def __init__(self):
        self.discount_factors = list()

    def add(self, discount_factor: DiscountFactor) -> None:
        self.discount_factors.append(discount_factor)

    def compute_discount_factor(self, start: date, end: date) -> DiscountFactor:
        # Interpolate using a preferred method CONSTANT_FORWARD_RATES
        pass


