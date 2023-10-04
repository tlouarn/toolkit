from decimal import Decimal

from definitions.date import Date
from definitions.discount_curve import DiscountCurve, Interpolation
from definitions.discount_factor import DiscountFactor
from definitions.interest_rate import Compounding, DayCount, InterestRate
from definitions.period import Period


def test_construct_discount_curve():
    # Rates curve (ACT/360 and annual compounding)
    quotes = {
        "1W": Decimal("0.03889"),
        "1M": Decimal("0.03872"),
        "3M": Decimal("0.03964"),
        "6M": Decimal("0.04128"),
        "12M": Decimal("0.04208"),
    }

    # Define start date
    start = Date(2023, 10, 3)

    # Create InterestRate objects
    interest_rates = {}
    for period, rate in quotes.items():
        interest_rates[period] = InterestRate(rate=rate, day_count=DayCount.ACT_360, compounding=Compounding.ANNUAL)

    # Build discount curve
    discount_factors = []
    for period, rate in interest_rates.items():
        discount_factor = DiscountFactor.from_interest_rate(
            start=start, end=start + Period.parse(period), interest_rate=rate
        )
        discount_factors.append(discount_factor)

    # Build discount curve
    discount_curve = DiscountCurve(discount_factors=discount_factors, interpolation=Interpolation.FLAT_FORWARD)

    # Get discount factor
    discount_factor = discount_curve.get_df(start=start, end=end)
    a = 1


def test_financepy():
    from financepy.market.curves import DiscountCurve

    discount_curve = DiscountCurve()
