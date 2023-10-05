from definitions.date import Date
from definitions.date_range import DateRange


def test_construct_date_range():
    start_date = Date(2020, 1, 1)
    end_date = Date(2021, 1, 1)
    date_range = DateRange(start_date, end_date)

    assert Date(2020, 1, 1) in date_range
    assert Date(2020, 2, 1) in date_range
    assert Date(2021, 1, 1) not in date_range
