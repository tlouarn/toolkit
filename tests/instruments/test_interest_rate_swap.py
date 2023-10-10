from decimal import Decimal

from holidays import country_holidays
from money import Money

from definitions.business_day_convention import BusinessDayConvention
from definitions.date import Date
from definitions.day_count import DayCountConvention
from definitions.interest_rate import InterestRate
from definitions.payment_frequency import PaymentFrequency
from definitions.period import Period
from definitions.schedule import generate_schedule
from definitions.stub import StubConvention
from instruments.interest_rate_swap import FixedLeg


def test_instantiate_fixed_floating_irs():
    # http://www.derivativepricing.com/blogpage.asp?id=8

    # Commong parameters
    effective_date = Date(2011, 11, 14)
    tenor = Period.parse("5Y")
    payment_frequency = PaymentFrequency("SemiAnnual")
    holidays = country_holidays("US")

    schedule = generate_schedule(
        start=effective_date,
        tenor=tenor,
        step=Period.parse("6M"),
        holidays=holidays,
        adjustment=BusinessDayConvention.MODIFIED_FOLLOWING,
        stub=StubConvention.FRONT,
    )

    fixed_leg = FixedLeg(
        effective_date=effective_date,
        notional=Money(1_000_000, "USD"),
        coupon=InterestRate(Decimal("0.0124")),
        schedule=schedule,
        day_count=DayCountConvention.THIRTY_I_360,
    )

    coupons = fixed_leg.coupons

    a = 1
