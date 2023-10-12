# https://www.r-bloggers.com/2021/07/interest-rate-swap-pricing-using-r-code/
from decimal import Decimal
from enum import Enum

from holidays import financial_holidays, HolidayBase
from money import Money

from definitions.adjustment import BusinessDayConvention
from definitions.date import Date
from definitions.interest_rate import InterestRate, CompoundingFrequency, DayCount
from definitions.period import Period


class Frequency(str, Enum):
    ANNUAL = "Annual"
    SEMI_ANNUAL = "SemiAnnual"



class FixedLeg:

    def __init__(self, notional: Money, value_date: Date, tenor: Period, coupon: InterestRate, holidays: HolidayBase):
        pass


fixed_leg = FixedLeg(
    notional=Money(10_000_000, "USD"),
    value_date=Date(2021, 7, 2),
    tenor=Period.parse("5Y"),
    coupon=InterestRate(Decimal("0.96495"), Frequency("SemiAnnual"), DayCount("30E/360")),
    holidays=financial_holidays("US")
)

from instruments.ois import make_ois_schedule

schedule = make_ois_schedule(
    Date(2021, 7, 2), tenor=Period.parse("5Y"), step=Period.parse("6M"), holidays=financial_holidays("US"),
    adjustment=BusinessDayConvention("ModifiedFollowing"))

a = 1

schedule = make_ois_schedule(
    start_date=Date(2021, 7, 2),
    tenor=Period.parse("3M"),
    step=Period.parse("6M"),
    holidays=financial_holidays("US"),
    adjustment=BusinessDayConvention("ModifiedFollowing")
)

# First zero rate
from definitions.day_count import compute_year_fraction

start = Date(2021, 7, 2)
end = Date(2021, 10, 4)

period = end - start
days = period.days

fraction = compute_year_fraction(start, end, DayCount("30E/360"))

interest_rate = InterestRate(Decimal("0.0014575"), CompoundingFrequency("Yearly"), DayCount("30E/360"))

zero_rate = (1 + interest_rate.rate * fraction)

a = 1
