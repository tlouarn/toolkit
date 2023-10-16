import pytest
from holidays import financial_holidays

from definitions.business_day import BusinessDayConvention, adjust_date
from definitions.date import Date

# TODO implement
# https://github.com/lballabio/QuantLib/blob/master/test-suite/businessdayconventions.cpp

def test_instantiate_convention():
    """
    BusinessDayConvention inherits from both str and Enum.
    """
    convention = BusinessDayConvention("ModifiedFollowing")

    assert convention == "ModifiedFollowing"
    assert convention == BusinessDayConvention.MODIFIED_FOLLOWING


def test_unknown_convention_should_raise_error():
    with pytest.raises(ValueError):
        convention = BusinessDayConvention("ModifiedUnadjusted")


def test_adjust_date():
    date = Date(2023, 12, 25)
    holidays = financial_holidays("ECB")
    convention = BusinessDayConvention.MODIFIED_FOLLOWING

    adjusted_date = adjust_date(date=date, holidays=holidays, convention=convention)

    assert adjusted_date == Date(2023, 12, 27)
