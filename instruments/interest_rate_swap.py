from dataclasses import dataclass

from money import Money

from definitions.benchmark import Benchmark
from definitions.date import Date
from definitions.day_count import DayCountConvention, year_fraction
from definitions.interest_rate import InterestRate
from definitions.payment_frequency import PaymentFrequency
from definitions.schedule import Schedule

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
    amount: Money


@dataclass
class FixedLeg:
    effective_date: Date
    notional: Money
    coupon: InterestRate
    schedule: Schedule
    day_count: DayCountConvention

    @property
    def coupons(self) -> list[Coupon]:
        coupons = []
        start_dates = [self.effective_date] + [date for date in self.schedule[:-1]]
        end_dates = [date for date in self.schedule]

        for dates in zip(start_dates, end_dates):
            fraction = year_fraction(dates[0], dates[1], self.day_count)
            coupon = Coupon(start=dates[0], end=dates[1], amount=self.notional * self.coupon.rate * fraction)
            coupons.append(coupon)

        return coupons


@dataclass
class FloatingLeg:
    benchmark: Benchmark
    spread: InterestRate
    payment_frequency: PaymentFrequency
    day_count: DayCountConvention


class FixedFloatingInterestRateSwap:
    def __init__(self, effective: Date, maturity: Date, fixed_leg: FixedLeg, floating_leg: FloatingLeg) -> None:
        self.effective = effective
        self.maturity = maturity
        self.fixed_leg = fixed_leg
        self.floating_leg = floating_leg

    def solve(self):
        pass
