from decimal import Decimal

from definitions.date import Date
from definitions.discount_curve import DiscountCurve, Interpolation
from definitions.discount_factor import DiscountFactor


def test_instantiate_discount_curve():
    # http://www.derivativepricing.com/blogpage.asp?id=6
    discount_factors = [
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2011, 11, 10), factor=Decimal(1)),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2011, 11, 14), factor=Decimal("0.9999843")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2012, 5, 14), factor=Decimal("0.9966889")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2012, 11, 14), factor=Decimal("0.9942107")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2013, 5, 14), factor=Decimal("0.9911884")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2013, 11, 14), factor=Decimal("0.9880738")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2014, 5, 14), factor=Decimal("0.983649")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2014, 11, 14), factor=Decimal("0.9786276")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2015, 5, 14), factor=Decimal("0.9710461")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2015, 11, 16), factor=Decimal("0.9621778")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2016, 5, 16), factor=Decimal("0.9514315")),
        DiscountFactor(start=Date(2011, 11, 10), end=Date(2016, 11, 14), factor=Decimal("0.9394919")),
    ]

    discount_curve = DiscountCurve(discount_factors=discount_factors, interpolation=Interpolation.FLAT_FORWARD)

    assert isinstance(discount_curve, DiscountCurve)


# def test_construct_discount_curve():
#     # Rates curve (ACT/360 and annual compounding)
#     quotes = {
#         "1W": Decimal("0.03889"),
#         "1M": Decimal("0.03872"),
#         "3M": Decimal("0.03964"),
#         "6M": Decimal("0.04128"),
#         "12M": Decimal("0.04208"),
#     }
#
#     # Define start date
#     start = Date(2023, 10, 3)
#
#     # Create InterestRate objects
#     interest_rates = {}
#     for period, rate in quotes.items():
#         interest_rates[period] = InterestRate(rate=rate, day_count=DayCount.ACTUAL_360, compounding=Compounding.YEARLY)
#
#     # Build discount curve
#     discount_factors = []
#     for period, rate in interest_rates.items():
#         discount_factor = DiscountFactor.from_interest_rate(
#             start=start, end=start + Period.parse(period), interest_rate=rate
#         )
#         discount_factors.append(discount_factor)
#
#     # Build discount curve
#     discount_curve = DiscountCurve(discount_factors=discount_factors, interpolation=Interpolation.FLAT_FORWARD)
#
#     # Get discount factor
#     discount_factor = discount_curve.get_df(start=start, end=end)
#     a = 1
#
#
# def test_financepy():
#     from financepy.market.curves import DiscountCurve
#
#     discount_curve = DiscountCurve()
