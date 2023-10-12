from __future__ import annotations

from decimal import Decimal
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
    def __init__(self, discount_factors: list[DiscountFactor]):
        """
        Construct a discount curve from a list of discount factors.
        :param discount_factors: list[DiscountFactor]
        """
        # Chek that there are discount factors
        if len(discount_factors) == 0:
            raise ValueError("No discount factors were provided.")

        # Check that all discount factors have the same start date
        if len(set(df.start for df in discount_factors)) != 1:
            raise ValueError("All discount factors must have the same start date.")

        # Check that all discount factors have a different end date
        if len(set(df.end for df in discount_factors)) < len(discount_factors):
            raise ValueError("All discount factors must have a different end date.")

        # Sort the discount factors by increasing end date
        self.discount_factors = sorted(discount_factors, key=lambda x: x.end)

    @property
    def start(self) -> Date:
        """
        All discount factors share the same start date.
        :return: The start date as a Date object.
        """
        return self.discount_factors[0].start

    def get(self, date: Date) -> DiscountFactor:
        # If the requested date is one of the inputs,
        # return the discount factor
        end_dates = [discount_factor.end for discount_factor in self.discount_factors]
        if date in end_dates:
            return [discount_factor for discount_factor in self.discount_factors if discount_factor.end == date][0]

        # If the requested date is outside the range of inputs,
        # raise an Exception
        if date < end_dates[0] or date > end_dates[-1]:
            raise ValueError(f"The date needs to be between {end_dates[0]} and {end_dates[-1]}")

        # Compute the number of days
        period = date - self.start
        days = period.days

        # Find the neighbouring data points
        i = 1
        while self.discount_factors[i].end <= date:
            i += 1

        prev_df = self.discount_factors[i - 1]
        next_df = self.discount_factors[i]

        prev_rate = prev_df.to_rate()
        next_rate = next_df.to_rate()

        dt = next_df.days - prev_df.days
        rate = ((next_df.days - days) * prev_rate.rate + (days - prev_df.days) * next_rate.rate) / dt
        df = Decimal.exp(-rate * days / Decimal(360))

        return DiscountFactor(start=self.start, end=date, factor=df)

    def forward(self, start: Date, end: Date) -> DiscountFactor:
        """
        Compute a forward-starting discount factor.

        :param start: start date
        :param end: end date
        :return: a forward-starting discount factor
        """
        factor = self.get(end).factor / self.get(start).factor
        return DiscountFactor(start=start, end=end, factor=factor)

    # def forward_rate(self, start: Date, end: Date, day_count: DayCountConvention, compounding: Compounding) -> InterestRate:
    #     """
    #     Compute a forward-starting interest rate from the curve.
    #     :param start: start date
    #     :param end: end date
    #     :param day_count: day count convention
    #     :param compounding: compounding frequency
    #     :return: a forward-starting interest rate
    #     """
    #
    #     forward_df = self.forward(start, end)
    #     return forward_df.to_rate()
