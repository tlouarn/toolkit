from decimal import Decimal

from holidays import country_holidays
from money import Money

from definitions.business_day_convention import BusinessDayConvention
from definitions.date import Date
from definitions.day_count import DayCountConvention
from definitions.interest_rate import InterestRate
from definitions.payment_frequency import PaymentFrequency
from definitions.period import Period
from instruments.interest_rate_swap import FixedLeg


def test_instantiate_fixed_floating_irs():
    # http://www.derivativepricing.com/blogpage.asp?id=8

    # Common parameters
    start = Date(2011, 11, 14)
    maturity = start + Period.parse("5Y")
    notional = Money(1_000_000, "USD")
    fixed_rate = InterestRate(InterestRate("0.0124"))

    # Generate fixed leg
    fixed_leg = FixedLeg.generate(
        start=start,
        maturity=maturity,
        notional=notional,
        coupon_rate=fixed_rate,
        day_count=DayCountConvention.THIRTY_I_360,
        payment_frequency=PaymentFrequency.SEMI_ANNUAL,
        convention=BusinessDayConvention.MODIFIED_FOLLOWING,
        holidays=country_holidays("US"),
    )

    floating_leg = FloatingLeg.generate(
        start=start,
        maturity=maturity,
        notional=notional,
        day_count=DayCountConvention.THIRTY_I_360,
        payment_frequency=PaymentFrequency.SEMI_ANNUAL,
        convention=BusinessDayConvention.MODIFIED_FOLLOWING,
        holidays=country_holidays("US"),
    )

    swap = InterestRateSwap(fixed_leg=fixed_leg, floating_leg=floating_leg)

    swap = libor_usd_3m_swap(start=start, tenor=tenor)
    value = swap.price(discount_curve)

    while value > 0:
        swap.update_fixed_coupon()

    swap = LiborUsd3MSwap()
    swap = EuriborSixMonthsSwap(start=start, tenor=tenor)
