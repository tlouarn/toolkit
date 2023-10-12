import math
from decimal import Decimal

from definitions.date import Date
from definitions.discount_factor import DiscountFactor
from definitions.interest_rate import InterestRate
from definitions.frequency import Frequency


def test_constructor():
    start = Date(2023, 9, 18)
    end = Date(2023, 10, 18)
    factor = Decimal("0.99")

    discount_factor = DiscountFactor(start=start, end=end, factor=factor)

    assert discount_factor.start == start
    assert discount_factor.end == end
    assert discount_factor.factor == factor


def test_construct_from_interest_rate():
    rate = Decimal("0.03")
    compounding = Frequency.ANNUAL
    interest_rate = InterestRate(rate=rate, compounding=compounding)

    start = Date(2023, 9, 18)
    end = Date(2023, 10, 18)
    discount_factor = DiscountFactor.from_interest_rate(start=start, end=end, interest_rate=interest_rate)

    assert discount_factor.factor == Decimal(1) / (Decimal(1) + Decimal("0.0025"))


def test_to_rate():
    start = Date(2023, 1, 1)
    end = Date(2023, 2, 1)
    factor = Decimal("0.999")
    discount_factor = DiscountFactor(start=start, end=end, factor=factor)

    rate = Decimal("0.01161871355129264709843463263")

    assert discount_factor.to_rate() == InterestRate(rate, Frequency.CONTINUOUS)

    import QuantLib as ql

    rate = ql.InterestRate(0.01161871355129264709843463263, ql.Actual360(), ql.Compounded, ql.Continuous)
    start = ql.Date(1, 1, 2023)
    end = ql.Date(1, 2, 2023)
    df = rate.discountFactor(start, end)

    assert math.isclose(df, 0.999)

    a = 1


def test_interpolate():
    import QuantLib as ql

    todays_date = ql.Date(12, 3, 2020)
    spot_dates = [todays_date + ql.Period(i, ql.Years) for i in [0, 1, 2, 3, 4, 5]]
    spot_rates = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]
    spot_curve = ql.ZeroCurve(
        spot_dates, spot_rates, ql.SimpleDayCounter(), ql.NullCalendar(), ql.Linear(), ql.Continuous, ql.Annual
    )

    a = 1
