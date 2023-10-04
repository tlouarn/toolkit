from holidays import financial_holidays

from definitions import Adjustment, Date, Period
from definitions.schedule import generate_performance_flows


def test_build_schedule():
    """
    Build a performance schedule for a 1Y ELS with monthly resets.
    """
    start = Date.today()
    maturity = start + Period.parse("1Y")
    frequency = Period.parse("1M")
    calendar = financial_holidays("ECB")
    adjustment = Adjustment.MODIFIED_FOLLOWING
    offset = Period.parse("2D")

    # TODO include check on weekdays

    schedule = generate_performance_flows(
        start=start, maturity=maturity, frequency=frequency, holidays=calendar, adjustment=adjustment, offset=offset
    )

    a = 1

