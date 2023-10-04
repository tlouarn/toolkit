import datetime as dt

import pytest

from definitions.date import Date, InvalidDateString
from definitions.period import Days, Period


def test_create_date():
    date = Date(2023, 9, 18)

    assert date.year == 2023
    assert date.month == 9
    assert date.day == 18


def test_parse_valid_date_string():
    date = Date.parse("2023-09-18")

    assert date.year == 2023
    assert date.month == 9
    assert date.day == 18


def test_parse_invalid_date_string():
    with pytest.raises(InvalidDateString):
        date = Date.parse("20230918")


def test_parse_invalid_date_string_2():
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


def test_instantiate_imm_date():
    date = Date.imm(12, 2023)

    assert date == Date(2023, 12, 20)


def test_constructor_third_friday():
    date = Date.third_friday(12, 2023)

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
