from decimal import Decimal

from definitions.date import Date
from definitions.day_count import DayCount, year_fraction


def test_construct_daycount():
    day_count = DayCount("ACT/365")

    assert day_count == DayCount.ACT_365


def test_compute_year_fraction_act_360():
    start_date = Date(2023, 9, 18)
    end_date = Date(2023, 10, 17)
    day_count = DayCount.ACT_360

    fraction = year_fraction(start_date, end_date, day_count)

    assert fraction == Decimal(29 / 360)


def test_compute_year_fraction_act_365():
    start_date = Date(2023, 9, 18)
    end_date = Date(2023, 10, 17)
    day_count = DayCount.ACT_365

    fraction = year_fraction(start_date, end_date, day_count)

    assert fraction == Decimal(29 / 365)


def test_compute_year_fraction_act_act():
    # Example from
    # https://academybooks.nl/test/Diploma/Book-Interest%20calcs.pdf

    start_date = Date(2007, 10, 1)
    end_date = Date(2008, 4, 1)
    day_count = DayCount.ACT_ACT

    fraction = year_fraction(start_date, end_date, day_count)

    assert fraction == Decimal(92 / 365) + Decimal(91 / 366)
