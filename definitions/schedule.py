from holidays import HolidayBase

from definitions.business_day_convention import BusinessDayConvention, adjust_date
from definitions.date import Date
from definitions.period import Period
from definitions.stub import StubConvention

# A schedule is a list of dates
Schedule = list[Date]


def generate_schedule(
    start: Date,
    maturity: Date,
    step: Period,
    holidays: HolidayBase,
    bus_day: BusinessDayConvention,
    stub: StubConvention,
) -> Schedule:
    """
    Generate a payment Schedule.

    :param start: Date
    :param maturity: Date
    :param step: Period used to compute the regular steps (e.g. "3M")
    :param holidays: List of holidays
    :param bus_day: BusinessDayConvention adjustment
    :param stub: Front or Back stub
    :return: An ordered list of Date
    """
    # Initialize schedule
    schedule = []

    # Adjust maturity
    maturity = adjust_date(maturity, holidays, bus_day)
    schedule.append(maturity)

    # Exit if the maturity is closer than a step
    if maturity < start + step:
        return schedule

    # If the stub is FRONT, compute regular periods
    # starting from the maturity
    if stub == StubConvention.FRONT:
        date = maturity - step
        while date > start:
            schedule.append(date)
            date = date - step

    # If the stub is BACK, compute regular periods
    # starting from the start date
    elif stub == StubConvention.BACK:
        date = start + step
        while date < maturity:
            schedule.append(date)
            date = date + step

    # Adjust intermediary payment dates
    schedule = [adjust_date(date, holidays, bus_day) for date in schedule]

    # Sort the payment dates
    return sorted(schedule)
