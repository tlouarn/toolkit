from decimal import Decimal

from definitions.date import Date
from definitions.day_count import DayCount, year_fraction


def test_construct_daycount():
    day_count = DayCount("ACT/365")

    assert day_count == DayCount.ACTUAL_365


def test_compute_year_fraction_actual_360():
    # All examples are coming from the following ISDA educational spreadsheet
    # https://www.isda.org/a/mIJEE/30-360-2006ISDADefs.xls

    assert year_fraction(Date(2007, 1, 15), Date(2007, 1, 30), DayCount.THIRTY_360) == Decimal(15) / Decimal(360)
    assert year_fraction(Date(2007, 1, 15), Date(2007, 2, 15), DayCount.THIRTY_360) == Decimal(31) / Decimal(360)
    assert year_fraction(Date(2007, 1, 15), Date(2007, 7, 15), DayCount.THIRTY_360) == Decimal(181) / Decimal(360)
    assert year_fraction(Date(2007, 9, 30), Date(2008, 3, 31), DayCount.THIRTY_360) == Decimal(183) / Decimal(360)
    assert year_fraction(Date(2007, 9, 30), Date(2007, 10, 31), DayCount.THIRTY_360) == Decimal(31) / Decimal(360)
    assert year_fraction(Date(2007, 9, 30), Date(2008, 9, 30), DayCount.THIRTY_360) == Decimal(366) / Decimal(360)
    assert year_fraction(Date(2007, 1, 15), Date(2007, 1, 31), DayCount.THIRTY_360) == Decimal(16) / Decimal(360)
    assert year_fraction(Date(2007, 1, 31), Date(2007, 2, 28), DayCount.THIRTY_360) == Decimal(28) / Decimal(360)
    assert year_fraction(Date(2007, 2, 28), Date(2007, 3, 31), DayCount.THIRTY_360) == Decimal(31) / Decimal(360)
    assert year_fraction(Date(2006, 8, 31), Date(2007, 2, 28), DayCount.THIRTY_360) == Decimal(181) / Decimal(360)
    assert year_fraction(Date(2007, 2, 28), Date(2007, 8, 31), DayCount.THIRTY_360) == Decimal(184) / Decimal(360)
    assert year_fraction(Date(2007, 2, 14), Date(2007, 2, 28), DayCount.THIRTY_360) == Decimal(14) / Decimal(360)
    assert year_fraction(Date(2007, 2, 26), Date(2008, 2, 29), DayCount.THIRTY_360) == Decimal(368) / Decimal(360)
    assert year_fraction(Date(2008, 2, 29), Date(2009, 2, 28), DayCount.THIRTY_360) == Decimal(365) / Decimal(360)
    assert year_fraction(Date(2008, 2, 29), Date(2008, 3, 30), DayCount.THIRTY_360) == Decimal(30) / Decimal(360)
    assert year_fraction(Date(2008, 2, 29), Date(2008, 3, 31), DayCount.THIRTY_360) == Decimal(31) / Decimal(360)
    assert year_fraction(Date(2007, 2, 28), Date(2007, 3, 5), DayCount.THIRTY_360) == Decimal(5) / Decimal(360)
    assert year_fraction(Date(2007, 10, 31), Date(2007, 11, 28), DayCount.THIRTY_360) == Decimal(28) / Decimal(360)
    assert year_fraction(Date(2007, 8, 31), Date(2008, 2, 29), DayCount.THIRTY_360) == Decimal(182) / Decimal(360)
    assert year_fraction(Date(2008, 2, 29), Date(2008, 8, 31), DayCount.THIRTY_360) == Decimal(184) / Decimal(360)
    assert year_fraction(Date(2008, 8, 31), Date(2009, 2, 28), DayCount.THIRTY_360) == Decimal(181) / Decimal(360)
    assert year_fraction(Date(2009, 2, 28), Date(2009, 8, 31), DayCount.THIRTY_360) == Decimal(184) / Decimal(360)


def test_compute_year_fraction_act_365():
    start_date = Date(2023, 9, 18)
    end_date = Date(2023, 10, 17)
    day_count = DayCount.ACTUAL_365

    fraction = year_fraction(start_date, end_date, day_count)

    assert fraction == Decimal(29 / 365)


def test_compute_year_fraction_act_act():
    # Example from
    # https://academybooks.nl/test/Diploma/Book-Interest%20calcs.pdf

    start_date = Date(2007, 10, 1)
    end_date = Date(2008, 4, 1)
    day_count = DayCount.ACTUAL_ACTUAL

    fraction = year_fraction(start_date, end_date, day_count)

    assert fraction == Decimal(92 / 365) + Decimal(91 / 366)


def test_compute_year_fraction_eurobond_basis():
    # All examples are coming from the following ISDA educational spreadsheet
    # https://www.isda.org/a/mIJEE/30-360-2006ISDADefs.xls

    assert year_fraction(Date(2007, 1, 15), Date(2007, 1, 30), DayCount.THIRTY_360) == Decimal(15) / Decimal(360)
    assert year_fraction(Date(2007, 1, 15), Date(2007, 2, 15), DayCount.THIRTY_360) == Decimal(30) / Decimal(360)
    assert year_fraction(Date(2007, 1, 15), Date(2007, 7, 15), DayCount.THIRTY_360) == Decimal(180) / Decimal(360)
    assert year_fraction(Date(2007, 9, 30), Date(2008, 3, 31), DayCount.THIRTY_360) == Decimal(180) / Decimal(360)
    assert year_fraction(Date(2007, 9, 30), Date(2007, 10, 31), DayCount.THIRTY_360) == Decimal(30) / Decimal(360)
    assert year_fraction(Date(2007, 9, 30), Date(2008, 9, 30), DayCount.THIRTY_360) == Decimal(360) / Decimal(360)
    assert year_fraction(Date(2007, 1, 15), Date(2007, 1, 31), DayCount.THIRTY_360) == Decimal(15) / Decimal(360)
    assert year_fraction(Date(2007, 1, 31), Date(2007, 2, 28), DayCount.THIRTY_360) == Decimal(28) / Decimal(360)
    assert year_fraction(Date(2007, 2, 28), Date(2007, 3, 31), DayCount.THIRTY_360) == Decimal(32) / Decimal(360)
    assert year_fraction(Date(2006, 8, 31), Date(2007, 2, 28), DayCount.THIRTY_360) == Decimal(178) / Decimal(360)
    assert year_fraction(Date(2007, 2, 28), Date(2007, 8, 31), DayCount.THIRTY_360) == Decimal(182) / Decimal(360)
    assert year_fraction(Date(2007, 2, 14), Date(2007, 2, 28), DayCount.THIRTY_360) == Decimal(14) / Decimal(360)
    assert year_fraction(Date(2007, 2, 26), Date(2008, 2, 29), DayCount.THIRTY_360) == Decimal(363) / Decimal(360)
    assert year_fraction(Date(2008, 2, 29), Date(2009, 2, 28), DayCount.THIRTY_360) == Decimal(359) / Decimal(360)
    assert year_fraction(Date(2008, 2, 29), Date(2008, 3, 30), DayCount.THIRTY_360) == Decimal(31) / Decimal(360)
    assert year_fraction(Date(2008, 2, 29), Date(2008, 3, 31), DayCount.THIRTY_360) == Decimal(31) / Decimal(360)
    assert year_fraction(Date(2007, 2, 28), Date(2007, 3, 5), DayCount.THIRTY_360) == Decimal(7) / Decimal(360)
    assert year_fraction(Date(2007, 10, 31), Date(2007, 11, 28), DayCount.THIRTY_360) == Decimal(28) / Decimal(360)
    assert year_fraction(Date(2007, 8, 31), Date(2008, 2, 29), DayCount.THIRTY_360) == Decimal(179) / Decimal(360)
    assert year_fraction(Date(2008, 2, 29), Date(2008, 8, 31), DayCount.THIRTY_360) == Decimal(181) / Decimal(360)
    assert year_fraction(Date(2008, 8, 31), Date(2009, 2, 28), DayCount.THIRTY_360) == Decimal(178) / Decimal(360)
    assert year_fraction(Date(2009, 2, 28), Date(2009, 8, 31), DayCount.THIRTY_360) == Decimal(182) / Decimal(360)
