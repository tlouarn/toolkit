from definitions.period import Period, Unit


def test_create_period():
    period = Period(1, Unit.MONTH)

    assert period.quantity == 1
    assert period.unit == Unit.MONTH


def test_create_period_from_string():
    period = Period.parse("1W")

    assert period.quantity == 1
    assert period.unit == Unit.WEEK


def test_compare_periods():
    period_1d = Period(1, Unit.DAY)
    period_7d = Period(7, Unit.DAY)
    period_1w = Period(1, Unit.WEEK)
    period_1m = Period(1, Unit.MONTH)
    period_2m = Period(2, Unit.MONTH)
    period_18m = Period(18, Unit.MONTH)
    period_1y = Period(1, Unit.YEAR)
    period_2y = Period(2, Unit.YEAR)

    assert period_1d < period_1w
    assert period_1w < period_1m
    assert period_1m < period_1y
    assert period_1m < period_2m
    assert period_7d == period_1w
    assert period_1y < period_18m < period_2y


def test_sort_periods():
    period_1d = Period(1, Unit.DAY)
    period_7d = Period(7, Unit.DAY)
    period_30d = Period(30, Unit.DAY)
    period_1w = Period(1, Unit.WEEK)
    period_2w = Period(2, Unit.WEEK)
    period_1m = Period(1, Unit.MONTH)
    period_2m = Period(2, Unit.MONTH)
    period_3m = Period(3, Unit.MONTH)
    period_6m = Period(6, Unit.MONTH)
    period_9m = Period(9, Unit.MONTH)
    period_12m = Period(12, Unit.MONTH)
    period_18m = Period(18, Unit.MONTH)
    period_1y = Period(1, Unit.YEAR)
    period_2y = Period(2, Unit.YEAR)
    period_5y = Period(5, Unit.YEAR)
    period_10y = Period(10, Unit.YEAR)

    # Create an ordered list of periods
    periods = [
        period_1d,
        period_7d,
        period_1w,
        period_2w,
        period_30d,
        period_1m,
        period_2m,
        period_3m,
        period_6m,
        period_9m,
        period_12m,
        period_1y,
        period_18m,
        period_2y,
        period_5y,
        period_10y,
    ]

    # Create a copy of the list and sort it by string representation
    # e.g. 10Y, 1D, 1M, 1W etc.
    string_periods = sorted(periods.copy(), key=lambda x: str(x))

    # Check that sorting it back puts the periods back in order
    assert sorted(string_periods) == periods
