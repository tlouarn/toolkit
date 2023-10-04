from decimal import Decimal

from definitions.date import Date
from definitions.discount_factor import DiscountFactor
from definitions.interest_rate import Compounding, DayCount, InterestRate


def test_construct_discount_factor():
    start = Date(2023, 9, 18)
    end = Date(2023, 10, 18)
    factor = Decimal("0.99")

    discount_factor = DiscountFactor(start=start, end=end, factor=factor)

    assert discount_factor.start == start
    assert discount_factor.end == end
    assert discount_factor.factor == factor


def test_construct_from_interest_rate():
    rate = Decimal("0.03")
    day_count = DayCount("ACT/360")
    compounding = Compounding.ANNUAL
    interest_rate = InterestRate(rate=rate, day_count=day_count, compounding=compounding)

    start = Date(2023, 9, 18)
    end = Date(2023, 10, 18)

    discount_factor = DiscountFactor.from_interest_rate(start=start, end=end, interest_rate=interest_rate)

    assert discount_factor.factor == Decimal(1 / (1 + 0.0025))
