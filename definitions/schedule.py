from holidays import HolidayBase

from definitions.business_day_convention import BusinessDayConvention, adjust_date
from definitions.date import Date
from definitions.period import Period
from definitions.stub import StubConvention

# A schedule is a list of dates
Schedule = list[Date]


def generate_schedule(
    start: Date,
    tenor: Period,
    step: Period,
    holidays: HolidayBase,
    adjustment: BusinessDayConvention,
    stub: StubConvention,
) -> Schedule:
    """
    Generate a payment Schedule.

    :param start: Date
    :param tenor: Tenor expressed as a Period (e.g. "5Y")
    :param step: Period used to compute regular steps (e.g. "3M")
    :param holidays: List of holidays
    :param adjustment: BusinessDayConvention adjustment
    :param stub: Front or Back stub
    :return: An ordered list of Date
    """
    # Initialize schedule
    schedule = []

    # Ensure maturity is > start
    if tenor.quantity <= 0:
        raise ValueError(f"Schedule tenor cannot be negative (value received={str(tenor)}).")

    # Compute maturity
    maturity = start + tenor

    # Adjust maturity
    maturity = adjust_date(maturity, holidays, adjustment)
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
    schedule = [adjust_date(date, holidays, adjustment) for date in schedule]

    # Sort the payment dates
    return sorted(schedule)
