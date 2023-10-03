import pytest

from definitions.date import Date, InvalidDateString
from definitions.tenor import Tenor


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


def test_add_tenor():
    date = Date(2023, 9, 18)
    tenor = Tenor.parse("1M")
    maturity = date + tenor

    assert maturity == Date(2023, 10, 18)
