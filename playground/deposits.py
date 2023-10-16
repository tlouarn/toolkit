from money import EUR, Money

from definitions.business_calendar import BusinessCalendar
from definitions.business_day import BusinessDayConvention as Convention
from definitions.date import Date
from definitions.day_count import DayCountConvention as DayCount
from definitions.interest_rate import InterestRate


class Deposit:

    def __init__(self, start: Date, end: Date, notional: Money, rate: InterestRate, day_count: DayCount, calendar: BusinessCalendar):
        self.start = start
        self.end = end
        self.notional = notional
        self.rate = rate
        self.day_count = day_count
        self.calendar = calendar



deposit_1w = Deposit(
    start=Date(2023,10,16),
    end=Date(2023,10,23),
    notional=EUR(100_000_000),
    rate=InterestRate.annual("0.05"),
    day_count=DayCount("ACT/360"),
    calendar=BusinessCalendar("TARGET2", Convention("ModifiedFollowing")                              ))


continuous = InterestRate.annual("0.05").to_continuous()
continuous = Annual("0.05").to_continuous()

rate = InterestRate("0.05", "Annual" | "Simple" | "Continuous" | "Quarterly" | )


from toolkit import Date, InterestRate, Deposit

