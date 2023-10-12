from decimal import Decimal

from holidays import financial_holidays

from definitions.business_day import BusinessDayConvention, adjust_date
from definitions.date import Date
from definitions.day_count import DayCountConvention
from definitions.discount_curve import DiscountCurve
from definitions.discount_factor import DiscountFactor
from definitions.interest_rate import CompoundingFrequency
from definitions.period import Days, Months, Weeks, Years


def test_instantiate_discount_curve():
    """
    Example taken from:
    http://www.derivativepricing.com/blogpage.asp?id=6
    """
    # These discount factors come from the abovementionned article
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

    # Build the discount curve
    discount_curve = DiscountCurve(discount_factors=discount_factors)

    # Check that all input discount factors are correctly recalculated
    assert all(discount_curve.get(df.end).factor == df.factor for df in discount_factors)

    # Check that all input discount factors are correctly recalculated
    # as "forward-starting" discount factors with the same start date
    assert all(discount_curve.forward(df.start, df.end).factor == df.factor for df in discount_factors)


def test_quantnet_using_quantlib():
    """
    Example taken from page 90 of
    https://quantnet.com/attachments/dima-ql-intro-2-pdf.10296

    This example demonstrates how to build a discount curve using QuantLib in C++.
    Here, we recreate the example using python-quantlib.
    """
    import QuantLib as ql

    cal = ql.TARGET()
    today = ql.Date(11, ql.September, 2009)
    libor = ql.EURLibor1M()
    dc = libor.dayCounter()

    settlement_days = 2
    settlement = cal.advance(today, settlement_days, ql.Days)

    dates = [
        settlement,
        settlement + ql.Period(1, ql.Days),
        settlement + ql.Period(1, ql.Weeks),
        settlement + ql.Period(1, ql.Months),
        settlement + ql.Period(2, ql.Months),
        settlement + ql.Period(3, ql.Months),
        settlement + ql.Period(6, ql.Months),
        settlement + ql.Period(9, ql.Months),
        settlement + ql.Period(1, ql.Years),
        settlement + ql.Period(1, ql.Years) + ql.Period(3, ql.Months),
        settlement + ql.Period(1, ql.Years) + ql.Period(6, ql.Months),
        settlement + ql.Period(1, ql.Years) + ql.Period(9, ql.Months),
        settlement + ql.Period(2, ql.Years),
    ]

    dfs = [
        1,
        0.9999656,
        0.9999072,
        0.9996074,
        0.999004,
        0.9981237,
        0.9951358,
        0.9929456,
        0.9899849,
        0.9861596,
        0.9815178,
        0.9752363,
        0.9680804,
    ]

    # Test 1: zero rate
    tmp_date_1 = settlement + ql.Period(1, ql.Years) + ql.Period(3, ql.Months)
    curve = ql.DiscountCurve(dates, dfs, dc, cal)
    zero_rate = curve.zeroRate(tmp_date_1, dc, ql.Simple, ql.Annual)
    assert round(zero_rate.rate(), 8) == 0.01107998

    # Test 2: spot discount factor
    assert round(curve.discount(tmp_date_1), 5) == 0.98616

    # Test 3: forward rate
    tmp_date_2 = tmp_date_1 + ql.Period(3, ql.Months)
    forward_rate = curve.forwardRate(tmp_date_1, tmp_date_2, dc, ql.Continuous)
    assert round(forward_rate.rate(), 8) == 0.01887223


def test_quantnet_using_toolkit():
    """
    Example taken from page 90 of
    https://quantnet.com/attachments/dima-ql-intro-2-pdf.10296

    This example demonstrates how to build a discount curve using QuantLib in C++.
    Here, we implement the test using our toolkit.
    """
    start = Date(2009, 9, 11)

    holidays = financial_holidays("ECB")
    day_count = DayCountConvention.ACTUAL_360
    bus_day = BusinessDayConvention.MODIFIED_FOLLOWING

    settlement_date = start + Days(2)
    settlement_date = adjust_date(settlement_date, holidays, bus_day)

    unadjusted_dates = [
        settlement_date + Days(0),
        settlement_date + Days(1),
        settlement_date + Weeks(1),
        settlement_date + Months(1),
        settlement_date + Months(2),
        settlement_date + Months(3),
        settlement_date + Months(6),
        settlement_date + Months(9),
        settlement_date + Years(1),
        settlement_date + Months(15),
        settlement_date + Months(18),
        settlement_date + Months(21),
        settlement_date + Years(2),
    ]

    dfs = [
        Decimal("1"),
        Decimal("0.9999656"),
        Decimal("0.9999072"),
        Decimal("0.9996074"),
        Decimal("0.999004"),
        Decimal("0.9981237"),
        Decimal("0.9951358"),
        Decimal("0.9929456"),
        Decimal("0.9899849"),
        Decimal("0.9861596"),
        Decimal("0.9815178"),
        Decimal("0.9752363"),
        Decimal("0.9680804"),
    ]

    # Build discount factors
    discount_factors = []
    for date, df in zip(unadjusted_dates, dfs):
        end = adjust_date(date=date, holidays=holidays, convention=bus_day)
        discount_factor = DiscountFactor(start=settlement_date, end=end, factor=df)
        discount_factors.append(discount_factor)

    # Build discount curve
    discount_curve = DiscountCurve(discount_factors=discount_factors)

    # Test 1: zero rate
    date_1 = settlement_date + Years(1) + Months(3)
    date_1 = adjust_date(date_1, holidays, bus_day)
    discount_factor = discount_curve.get(date_1)
    zero_rate = discount_factor.to_rate().effective  #TODO fix
    assert zero_rate == Decimal("0.01107998")

    # Test 2: spot discount factor
    assert discount_curve.get(date_1).factor == Decimal("0.9861596")

    # Test 3: forward rate
    date_2 = date_1 + Months(3)
    expected = Decimal("0.01887223")
    actual = discount_curve.forward_rate(date_1, date_2, day_count, CompoundingFrequency.CONTINUOUS).rate
    assert round(actual, 8) == expected
