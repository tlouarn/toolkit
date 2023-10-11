import datetime

from holidays import country_holidays

from definitions.business_day_convention import BusinessDayConvention
from definitions.date import Date
from definitions.period import Period
from definitions.schedule import generate_schedule
from definitions.stub import StubConvention


def test_generate_schedules_3m_6m():
    """
    Generate a payment schedule for a 5Y LIBOR USD 3M fixed/floating IRS.
    https://www.r-bloggers.com/2021/07/interest-rate-swap-pricing-using-r-code/
    """

    # Common parameters
    start = Date(2021, 7, 2)
    maturity = start + Period.parse("5Y")
    holidays = country_holidays("US")
    holidays.update(datetime.date(2022, 1, 3))  # TODO fix, somehow 3 JAN 2022 is not seen as a holiday
    adjustment = BusinessDayConvention.MODIFIED_FOLLOWING
    stub = StubConvention.FRONT

    # The fixed leg schedule has semi-annual payments
    fixed_leg_schedule = generate_schedule(
        start=start, maturity=maturity, step=Period.parse("6M"), holidays=holidays, bus_day=adjustment, stub=stub
    )

    # The floating leg schedule has quarterly payments
    floating_leg_schedule = generate_schedule(
        start=start, maturity=maturity, step=Period.parse("3M"), holidays=holidays, bus_day=adjustment, stub=stub
    )

    assert fixed_leg_schedule == [
        Date.parse("2022-01-04"),
        Date.parse("2022-07-05"),
        Date.parse("2023-01-03"),
        Date.parse("2023-07-03"),
        Date.parse("2024-01-02"),
        Date.parse("2024-07-02"),
        Date.parse("2025-01-02"),
        Date.parse("2025-07-02"),
        Date.parse("2026-01-02"),
        Date.parse("2026-07-02"),
    ]

    assert floating_leg_schedule == [
        Date.parse("2021-10-04"),
        Date.parse("2022-01-04"),
        Date.parse("2022-04-04"),
        Date.parse("2022-07-05"),
        Date.parse("2022-10-03"),
        Date.parse("2023-01-03"),
        Date.parse("2023-04-03"),
        Date.parse("2023-07-03"),
        Date.parse("2023-10-02"),
        Date.parse("2024-01-02"),
        Date.parse("2024-04-02"),
        Date.parse("2024-07-02"),
        Date.parse("2024-10-02"),
        Date.parse("2025-01-02"),
        Date.parse("2025-04-02"),
        Date.parse("2025-07-02"),
        Date.parse("2025-10-02"),
        Date.parse("2026-01-02"),
        Date.parse("2026-04-02"),
        Date.parse("2026-07-02"),
    ]


def test_generate_schedule_6m():
    """
    Generate a payment schedule for a 5Y LIBOR USD 6M fixed/floating IRS.
    http://www.derivativepricing.com/blogpage.asp?id=8
    """

    # Common parameters
    start = Date(2011, 11, 14)
    maturity = start + Period.parse("5Y")
    step = Period.parse("6M")
    holidays = country_holidays("US")
    adjustment = BusinessDayConvention.MODIFIED_FOLLOWING
    stub = StubConvention.FRONT

    # Both the fixed and floating legs
    # share the same schedule
    schedule = generate_schedule(
        start=start, maturity=maturity, step=step, holidays=holidays, bus_day=adjustment, stub=stub
    )

    assert schedule == [
        Date.parse("2012-05-14"),
        Date.parse("2012-11-14"),
        Date.parse("2013-05-14"),
        Date.parse("2013-11-14"),
        Date.parse("2014-05-14"),
        Date.parse("2014-11-14"),
        Date.parse("2015-05-14"),
        Date.parse("2015-11-16"),
        Date.parse("2016-05-16"),
        Date.parse("2016-11-14"),
    ]
