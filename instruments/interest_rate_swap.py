from __future__ import annotations

from dataclasses import dataclass

from holidays import HolidayBase
from money import Money

from definitions.business_day import BusinessDayConvention, adjust_date
from definitions.date import Date
from definitions.day_count import DayCountConvention, compute_year_fraction
from definitions.discount_curve import DiscountCurve
from definitions.frequency import Frequency
from definitions.interest_rate import Decimal
from definitions.period import Period
from definitions.schedule import generate_schedule
from definitions.stub import StubConvention

"""
Modeling problem: actual swap object vs handlers to generate parts of the object.
For instance, ultimately a swap is a collection of coupons.
But when defining a swap, we do not use the coupons as such, we use the parameters 
required to generate the strip of coupons and expect a bijective equivalence between 
swap parameters and coupons dates and amounts.

Therefore we choose to model a Fixed/Floating swap as a sequence of coupons and we
provide generators to generate these swaps.

class FixedFloating:

    @classmethod
    def generate():
        # factory method
        pass

We can further abstract with usual swap market conventions.

def generate_libor_usd_3M_irs():
    pass


class LiborUsd3mSwap:
    
    def __init__():
        day_count = DayCountConvention("30I/360") for the fixed leg
        payment_frequency = Pay
        super().__init__()
"""


@dataclass
class Coupon:
    start: Date
    end: Date
    payment: Date
    amount: Money


# TODO replace convention and holidays with calendar
@dataclass
class FixedLeg:
    coupons: list[Coupon]

    @classmethod
    def generate(
        cls,
        start: Date,
        maturity: Date,
        notional: Money,
        coupon_rate: Decimal,
        day_count: DayCountConvention,
        payment_frequency: Frequency,
        payment_offset: Period,
        convention: BusinessDayConvention,
        holidays: HolidayBase,
    ) -> FixedLeg:
        """
        Generate a FixedLeg, i.e. a sequence of coupons.
        """
        # Get the period equivalent to the payment frequency
        step = payment_frequency.to_period()

        # Generate schedule
        schedule = generate_schedule(
            start=start,
            maturity=maturity,
            step=step,
            holidays=holidays,
            convention=convention,
            stub=StubConvention.FRONT,
        )

        # Generate coupons
        coupons = []
        start_dates = [start] + [date for date in schedule[:-1]]
        end_dates = [date for date in schedule]
        for dates in zip(start_dates, end_dates):
            fraction = compute_year_fraction(dates[0], dates[1], day_count)
            amount = notional * coupon_rate * fraction
            payment = adjust_date(dates[1] + payment_offset, holidays, convention)
            coupon = Coupon(start=dates[0], end=dates[1], amount=amount, payment=payment)
            coupons.append(coupon)

        # Return coupons
        return FixedLeg(coupons=coupons)

    def compute_npv(self, discount_curve: DiscountCurve) -> Decimal:
        npv = Decimal(0)

        for coupon in self.coupons:
            discount_factor = discount_curve.get(coupon.payment)
            npv += coupon.amount * discount_factor

        return npv


@dataclass
class FloatingCoupon:
    start: Date
    end: Date
    payment: Date
    spread: Decimal


@dataclass
class FloatingLeg:
    coupons: list[FloatingCoupon]
    day_count: DayCountConvention
    notional: Money

    @classmethod
    def generate(
        cls,
        start: Date,
        maturity: Date,
        notional: Money,
        spread: Decimal,
        day_count: DayCountConvention,
        payment_frequency: Frequency,
        payment_offset: Period,
        convention: BusinessDayConvention,
        holidays: HolidayBase,
    ) -> FloatingLeg:
        # Get the period equivalent to the payment frequency
        step = payment_frequency.to_period()

        # Generate schedule
        schedule = generate_schedule(
            start=start,
            maturity=maturity,
            step=step,
            holidays=holidays,
            convention=convention,
            stub=StubConvention.FRONT,
        )

        # Generate coupons
        coupons = []
        start_dates = [start] + [date for date in schedule[:-1]]
        end_dates = [date for date in schedule]
        for dates in zip(start_dates, end_dates):
            payment = adjust_date(dates[1] + payment_offset, holidays, convention)
            coupon = FloatingCoupon(start=dates[0], end=dates[1], payment=payment, spread=spread)
            coupons.append(coupon)

        # Return coupons
        return FloatingLeg(coupons=coupons, notional=notional, day_count=day_count)


# @dataclass
# class FixedLeg:
#     effective_date: Date
#     notional: Money
#     coupon: InterestRate
#     schedule: Schedule
#     day_count: DayCountConvention
#
#     @property
#     def coupons(self) -> list[Coupon]:
#         coupons = []
#         start_dates = [self.effective_date] + [date for date in self.schedule[:-1]]
#         end_dates = [date for date in self.schedule]
#
#         for dates in zip(start_dates, end_dates):
#             fraction = year_fraction(dates[0], dates[1], self.day_count)
#             coupon = Coupon(start=dates[0], end=dates[1], amount=self.notional * self.coupon.rate * fraction)
#             coupons.append(coupon)
#
#         return coupons


# class FixedFloatingInterestRateSwap:
#     def __init__(self, effective: Date, maturity: Date, fixed_leg: FixedLeg, floating_leg: FloatingLeg) -> None:
#         self.effective = effective
#         self.maturity = maturity
#         self.fixed_leg = fixed_leg
#         self.floating_leg = floating_leg
#
#     def solve(self):
#         pass


class InterestRateSwap:
    def __init__(self, way: str, fixed_leg: FixedLeg, floating_leg: FloatingLeg) -> None:
        self.way = way
        self.fixed_leg = fixed_leg
        self.floating_leg = floating_leg
