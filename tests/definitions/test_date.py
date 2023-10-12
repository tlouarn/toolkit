import datetime as dt

import pytest

from definitions.date import Date, InvalidDateString
from definitions.date_range import DateRange
from definitions.period import Days, Period
from tests.definitions.test_date_data import YEARS


def test_constructor():
    date = Date(2023, 9, 18)

    assert date.year == 2023
    assert date.month == 9
    assert date.day == 18


def test_invalid_date_raises_value_error():
    # Test month outside of bounds
    with pytest.raises(ValueError):
        date = Date(2023, 15, 15)

    # Test negative day value
    with pytest.raises(ValueError):
        date = Date(2023, 2, -1)

    # Test day value outside of bounds
    with pytest.raises(ValueError):
        date = Date(2023, 2, 32)

    # 2023 is not a leap year
    with pytest.raises(ValueError):
        date = Date(2023, 2, 29)


def test_parse_valid_date_string():
    date = Date.parse("2023-09-18")

    assert date.year == 2023
    assert date.month == 9
    assert date.day == 18


def test_parse_invalid_date_strings():
    with pytest.raises(InvalidDateString):
        date = Date.parse("20230918")

    with pytest.raises(InvalidDateString):
        date = Date.parse("YYYY 09 18")


def test_comparison_eq():
    date_1 = Date(2023, 9, 18)
    date_2 = Date(2023, 9, 18)

    assert date_1 is not date_2
    assert date_1 == date_2


def test_comparison_lt():
    date_1 = Date(2022, 9, 18)
    date_2 = Date(2023, 9, 18)
    date_3 = Date(2023, 9, 19)
    date_4 = Date(2023, 10, 18)

    assert date_1 < date_2 < date_3 < date_4


def test_add_period():
    date = Date(2023, 9, 18)
    period = Period.parse("1M")
    maturity = date + period

    assert maturity == Date(2023, 10, 18)


def test_subtract_period():
    date = Date(2023, 9, 18)
    period = Period.parse("1W")
    maturity = date - period

    assert maturity == Date(2023, 9, 11)


def test_subtract_date():
    date_1 = Date(2023, 9, 18)
    date_2 = Date(2023, 10, 18)

    assert date_2 - date_1 == Days(30)


def test_constructor_imm_date():
    date = Date.imm(2023, 12)

    assert date == Date(2023, 12, 20)


def test_constructor_third_friday():
    date = Date.third_friday(2023, 12)

    assert date == Date(2023, 12, 15)


def test_str():
    date = Date(2023, 9, 18)

    assert str(date) == "2023-09-18"


def test_today():
    date = Date.today()

    assert date.to_date() == dt.date.today()


def test_weekday():
    assert Date(2023, 9, 18).weekday == "MON"
    assert Date(2023, 9, 19).weekday == "TUE"
    assert Date(2023, 9, 20).weekday == "WED"
    assert Date(2023, 9, 21).weekday == "THU"
    assert Date(2023, 9, 22).weekday == "FRI"
    assert Date(2023, 9, 23).weekday == "SAT"
    assert Date(2023, 9, 24).weekday == "SUN"


def test_is_weekend():
    assert not Date(2023, 9, 18).is_weekend
    assert not Date(2023, 9, 19).is_weekend
    assert not Date(2023, 9, 20).is_weekend
    assert not Date(2023, 9, 21).is_weekend
    assert not Date(2023, 9, 22).is_weekend
    assert Date(2023, 9, 23).is_weekend
    assert Date(2023, 9, 24).is_weekend


def test_is_leap_year():
    """
    Test data is coming from QuantLib.
    https://github.com/lballabio/QuantLib/blob/master/ql/time/date.cpp
    """
    # Check that the function is correct for all years
    # between 1901 and 2200
    assert all(Date(1901 + i, 1, 1).is_leap == is_leap for i, is_leap in enumerate(YEARS))


def test_is_eom():
    assert Date(2024, 1, 31).is_eom
    assert Date(2024, 2, 29).is_eom
    assert Date(2023, 2, 28).is_eom

    assert not Date(2024, 2, 28).is_eom
    assert not Date(2023, 1, 30).is_eom

    assert sum(1 if date.is_eom else 0 for date in DateRange(Date(2023, 1, 1), Date(2024, 1, 1))) == 12
    assert sum(1 if date.is_eom else 0 for date in DateRange(Date(2024, 1, 1), Date(2025, 1, 1))) == 12
