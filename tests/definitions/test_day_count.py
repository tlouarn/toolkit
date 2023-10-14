from decimal import Decimal

import pytest

from definitions.date import Date
from definitions.day_count import DayCountConvention, compute_year_fraction
from tests.definitions.test_day_count_data import ISDA_EXAMPLES


def test_construct_daycount():
    day_count = DayCountConvention("ACT/365")

    assert day_count == DayCountConvention.ACTUAL_365


@pytest.mark.parametrize("start_date,end_date,day_count,expected", ISDA_EXAMPLES)
def test_compute_year_fraction(start_date: Date, end_date: Date, day_count: DayCountConvention, expected: Decimal):
    assert compute_year_fraction(start_date, end_date, day_count) == expected


def test_compute_year_fraction_act_365():
    start_date = Date(2023, 9, 18)
    end_date = Date(2023, 10, 17)
    day_count = DayCountConvention.ACTUAL_365

    fraction = compute_year_fraction(start_date, end_date, day_count)

    assert fraction == Decimal(29) / Decimal(365)


def test_compute_year_fraction_act_act():
    # Example from
    # https://academybooks.nl/test/Diploma/Book-Interest%20calcs.pdf

    start_date = Date(2007, 10, 1)
    end_date = Date(2008, 4, 1)
    day_count = DayCountConvention.ACTUAL_ACTUAL_ISDA

    fraction = compute_year_fraction(start_date, end_date, day_count)

    assert fraction == Decimal(92) / Decimal(365) + Decimal(91) / Decimal(366)


def test_compute_year_fraction_actual_actual_isda():
    """
    Examples taken from:
    http://www.deltaquants.com/day-count-conventions

    #TODO implement all examples
    """
    start = Date(2007, 12, 28)
    end = Date(2008, 2, 29)
    fraction = compute_year_fraction(start=start, end=end, day_count=DayCountConvention.ACTUAL_ACTUAL_ISDA)
    assert round(fraction, 15) == Decimal(62 / 365)

    start = Date(2007, 10, 31)
    end = Date(2008, 11, 30)
    fraction = compute_year_fraction(start=start, end=end, day_count=DayCountConvention.ACTUAL_ACTUAL_ISDA)
    assert round(fraction, 15) == Decimal("1.08243131970956")

    a = 1
