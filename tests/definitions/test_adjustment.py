from holidays import financial_holidays

from definitions.adjustment import Adjustment, adjust
from definitions.date import Date


# TODO issue modifying in-place vs returning a new value


def test_create_adjustment():
    adjustment = Adjustment("ModifiedFollowing")

    assert adjustment == Adjustment.MODIFIED_FOLLOWING


def test_adjust():
    date = Date(2023, 12, 25)
    adjusted_date = adjust(date, financial_holidays("ECB"), Adjustment.MODIFIED_FOLLOWING)

    assert adjusted_date == Date(2023, 12, 27)
