from __future__ import annotations

from decimal import Decimal
from enum import Enum

from definitions.date import Date
from definitions.discount_factor import DiscountFactor
from definitions.interest_rate import InterestRate
from utils.interpolate import linear_interpolation

"""
Ways to instantiate a DiscountFactor:

From two cash-flows:
df = DiscountFactor.from_cashflows(cash_flow, cash_flow2)
df = DiscountFactor.from_interest_rate(interest_rate, start, end)


TODO maybe use a Protocol
DiscountCurve(Protocol):


DiscountCurve = FlatForward | LogLinearDiscountFactor | LinearDiscountFactor | 


"""


class Method(str, Enum):
    """
    List of available interpolation methods in order to compute
    discount factors from the discount curve.
    """

    LINEAR_ZERO_RATE = "LinearZeroRate"
    # LOG_LINEAR_ZERO_RATE = "LogLinearZeroRate"
    LINEAR_DISCOUNT_FACTOR = "LinearDiscountFactor"
    LOG_LINEAR_DISCOUNT_FACTOR = "LogLinearDiscountFactor"
    # LINEAR_SWAP_RATE = "LinearSwapRate"
    # LINEAR_FORWARD_RATE = "LinearForwardRate"


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

    def get(self, date: Date, method: Method) -> DiscountFactor:
        # TODO CHECK LOGLINEAR INTERPOLATION
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

        df1 = self.discount_factors[i - 1]
        df2 = self.discount_factors[i]

        x1 = Decimal(df1.days)
        x2 = Decimal(df2.days)
        x = Decimal(days)

        match method:
            case method.LINEAR_ZERO_RATE:
                """
                Linear interpolation of the zero rates.
                Zero rates are the continuously compounded spot rates inferred from
                the discount curve.
                """
                y1 = -Decimal.ln(df1.factor) / x1
                y2 = -Decimal.ln(df2.factor) / x2
                interp = linear_interpolation(x1, y1, x2, y2, x)
                y = Decimal.exp(-interp * x)

            case method.LINEAR_DISCOUNT_FACTOR:
                """
                Linear interpolation of the discount factors.
                """
                y1 = df1.factor
                y2 = df2.factor
                y = linear_interpolation(x1, y1, x2, y2, x)

            case method.LOG_LINEAR_DISCOUNT_FACTOR:
                """
                Linear interpolation of the natural logarithm of the discount factors.
                # TODO check also named "FLAT_FORWARD"
                """
                y1 = Decimal.ln(df1.factor)
                y2 = Decimal.ln(df2.factor)
                interp = linear_interpolation(x1, y1, x2, y2, x)
                y = Decimal.exp(interp)

            case _:
                raise NotImplementedError

        return DiscountFactor(start=self.start, end=date, factor=y)

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


class FlatForward:
    def __init__(self, start: Date, rate: InterestRate) -> None:
        self.start = start
        self.rate = rate

    def zero_discount_factor(self, date: Date) -> Decimal:
        if date <= self.start:
            raise ValueError

        return self.rate.to_discount_factor(self.start, date)

    def forward_discount_factor(self, start: Date, end: Date) -> Decimal:
        if not self.start <= start < end:
            raise ValueError

        return self.rate.to_discount_factor(start, end)
