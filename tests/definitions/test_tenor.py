from definitions.tenor import Tenor, Unit


def test_create_tenor():
    tenor = Tenor(1, Unit.MONTH)

    assert tenor.quantity == 1
    assert tenor.unit == Unit.MONTH


def test_create_tenor_from_string():
    tenor = Tenor.parse("1W")

    assert tenor.quantity == 1
    assert tenor.unit == Unit.WEEK


def test_compare_tenors():
    tenor_1d = Tenor(1, Unit.DAY)
    tenor_7d = Tenor(7, Unit.DAY)
    tenor_1w = Tenor(1, Unit.WEEK)
    tenor_1m = Tenor(1, Unit.MONTH)
    tenor_2m = Tenor(2, Unit.MONTH)
    tenor_18m = Tenor(18, Unit.MONTH)
    tenor_1y = Tenor(1, Unit.YEAR)
    tenor_2y = Tenor(2, Unit.YEAR)

    assert tenor_1d < tenor_1w
    assert tenor_1w < tenor_1m
    assert tenor_1m < tenor_1y
    assert tenor_1m < tenor_2m
    assert tenor_7d == tenor_1w
    assert tenor_1y < tenor_18m < tenor_2y


def test_sort_tenors():
    tenor_1d = Tenor(1, Unit.DAY)
    tenor_7d = Tenor(7, Unit.DAY)
    tenor_30d = Tenor(30, Unit.DAY)
    tenor_1w = Tenor(1, Unit.WEEK)
    tenor_2w = Tenor(2, Unit.WEEK)
    tenor_1m = Tenor(1, Unit.MONTH)
    tenor_2m = Tenor(2, Unit.MONTH)
    tenor_3m = Tenor(3, Unit.MONTH)
    tenor_6m = Tenor(6, Unit.MONTH)
    tenor_9m = Tenor(9, Unit.MONTH)
    tenor_12m = Tenor(12, Unit.MONTH)
    tenor_18m = Tenor(18, Unit.MONTH)
    tenor_1y = Tenor(1, Unit.YEAR)
    tenor_2y = Tenor(2, Unit.YEAR)
    tenor_5y = Tenor(5, Unit.YEAR)
    tenor_10y = Tenor(10, Unit.YEAR)

    # Create an ordered list of tenors
    tenors = [
        tenor_1d,
        tenor_7d,
        tenor_1w,
        tenor_2w,
        tenor_30d,
        tenor_1m,
        tenor_2m,
        tenor_3m,
        tenor_6m,
        tenor_9m,
        tenor_12m,
        tenor_1y,
        tenor_18m,
        tenor_2y,
        tenor_5y,
        tenor_10y,
    ]

    # Create a copy of the list and sort it by string representation
    # e.g. 10Y, 1D, 1M, 1W etc.
    string_tenors = sorted(tenors.copy(), key=lambda x: str(x))

    # Check that sorting it back puts the tenors back in order
    assert sorted(string_tenors) == tenors
