from holidays import financial_holidays

from definitions.adjustment import BusinessDayConvention, adjust_date
from definitions.date import Date


# TODO issue modifying in-place vs returning a new value


def test_create_adjustment():
    adjustment = BusinessDayConvention("ModifiedFollowing")

    assert adjustment == BusinessDayConvention.MODIFIED_FOLLOWING


def test_adjust():
    date = Date(2023, 12, 25)
    adjusted_date = adjust_date(date, financial_holidays("ECB"), BusinessDayConvention.MODIFIED_FOLLOWING)

    assert adjusted_date == Date(2023, 12, 27)
