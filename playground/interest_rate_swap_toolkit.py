# http://gouthamanbalaraman.com/blog/interest-rate-swap-quantlib-python.html
# Now we try to implement the above using our toolkit

from decimal import Decimal

from holidays import country_holidays
from money import Money

from definitions.business_calendar import BusinessCalendar
from definitions.business_day import BusinessDayConvention
from definitions.date import Date
from definitions.day_count import DayCountConvention
from definitions.discount_curve import FlatForward
from definitions.frequency import Frequency
from definitions.interest_rate import InterestRate
from definitions.period import Days, Years
from instruments.interest_rate_swap import FixedLeg, FloatingLeg, InterestRateSwap

calculation_date = Date(2015, 10, 20)
calendar = BusinessCalendar("US", BusinessDayConvention("ModifiedFollowing"))
settlement_date = calendar.add_business_days(calculation_date, 5)
maturity_date = calendar.add_period(settlement_date, Years(10))

notional = Money(10_000_000, "USD")
holidays = country_holidays("US")

fixed_leg = FixedLeg.generate(
    start=settlement_date,
    maturity=maturity_date,
    notional=notional,
    coupon_rate=Decimal("0.025"),
    day_count=DayCountConvention("ACT/360"),
    payment_frequency=Frequency("SemiAnnual"),
    payment_offset=Days(0),
    convention=BusinessDayConvention("ModifiedFollowing"),
    holidays=holidays,
)


a = 1

floating_leg = FloatingLeg.generate(
    start=settlement_date,
    maturity=maturity_date,
    notional=notional,
    spread=Decimal("0.004"),
    day_count=DayCountConvention("ACT/360"),
    payment_frequency=Frequency("Quarterly"),
    payment_offset=Days(0),
    convention=BusinessDayConvention("ModifiedFollowing"),
    holidays=holidays,
)

swap = InterestRateSwap(way="PAYER", fixed_leg=fixed_leg, floating_leg=floating_leg)


# Flatforward curve
forward_rate = InterestRate(Decimal("0.01"), DayCountConvention("ACT/365"), Frequency("Continuous"))
discount_curve = FlatForward(start=calculation_date, rate=forward_rate)
fixed_npv = fixed_leg.compute_npv(discount_curve)

ibor_rate = InterestRate(Decimal("0.02"), DayCountConvention("ACT/365"), Frequency("Continuous"))
ibor_curve = FlatForward(start=calculation_date, rate=ibor_rate)
floating_npv = floating_leg.compute_npv(ibor_curve, discount_curve)

# pricer = InterestRateSwapPricer(swap=swap, ibor_curve=ibor_curve, discount_curve=discount_curve)


a = 1
#
#
# fixed_schedule = generate_schedule(
#     start=settlement_date,
#     maturity=maturity_date,
#     step=Months(6),
#     holidays=country_holidays("US"),
#     convention=BusinessDayConvention("ModifiedFollowing"),
#     stub=StubConvention.BACK,
# )
#
# floating_schedule = generate_schedule(
#     start=settlement_date,
#     maturity=maturity_date,
#     step=Months(3),
#     holidays=country_holidays("US"),
#     convention=BusinessDayConvention("ModifiedFollowing"),
#     stub=StubConvention.BACK,
# )
#
# swap = InterestRateSwap(
#     way="PAYER",
#     notional=Money(10_000_000, "USD"),
#     fixed_schedule=fixed_schedule,
#     fixed_rate=Decimal(Decimal("0.025"), "ACT/360", "Annual"),
#     floating_schedule=floating_schedule,
#     floating_rate=FloatingRate( spread=spread, "ACT/360")
# )
#
#
#
#
# pricer = InterestRateSwapPricer()
# ibor_curve = DiscountCurve("EURIBOR")
# discount_curve = DiscountCurve("ESTER")
# pricer.price(swap, ibor_curve, discount_curve)
#
# # Define the swap as an object holding instrument details
# # price using a pricer: the pricer will:
# # - extract the schedule of the floating leg
# # - price each forward rate using the ibor curve
# # - discount each leg
# # - compute the npv
