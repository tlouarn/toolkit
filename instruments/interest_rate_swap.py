from dataclasses import dataclass

from money import Money

from definitions.benchmark import Benchmark
from definitions.date import Date
from definitions.day_count import DayCountConvention
from definitions.interest_rate import InterestRate
from definitions.payment_frequency import PaymentFrequency


@dataclass
class FixedLeg:
    notional: Money
    coupon: InterestRate
    payment_frequency: PaymentFrequency
    day_count: DayCountConvention



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
