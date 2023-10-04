from dataclasses import dataclass
from enum import Enum

from holidays import HolidayBase

from definitions.adjustment import Adjustment, adjust
from definitions.date import Date
from definitions.period import Period
from shared.exceptions import ToolkitException


class InvalidDates(ToolkitException):
    pass

class Stub(str, Enum):
    FRONT = "FRONT"
    BACK = "BACK"


@dataclass
class PerformanceFlow:
    start: Date
    end: Date
    payment: Date


@dataclass
class InterestRateFlow:
    fixing: Date
    start: Date
    end: Date
    payment: Date


@dataclass
class DividendFlow:
    start: Date
    end: Date
    payment: Date


Flow = PerformanceFlow | InterestRateFlow | DividendFlow
Schedule = list[Flow]


# class Schedule(list[Flow]):
#
#     def __init__(self, flows: list[Flow]):
#         self.flows = flows
#
#     @classmethod
#     def generate(cls, start: Date, end: Date, period: Period, holidays: HolidayBase, adjustment: Adjustment):
#         pass


@dataclass
class EquityLinkedSwapSchedule:
    performance: Schedule
    interest_rate: Schedule


def generate_performance_flows(
    start: Date,
    maturity: Date,
    frequency: Period,
    holidays: HolidayBase,
    adjustment: Adjustment,
    offset: Period,
) -> Schedule:
    """
    TODO: Add Stub.FRONT or Stub.BACK
    """
    if maturity <= start:
        raise InvalidDates(f"{maturity=} must be greater than {start=}")


    # Assuming the generation of dates is BACK_STUB
    # Generate the list of unadjusted reset dates
    resets = [start]
    period_end = start + frequency
    while period_end < maturity:
        resets.append(period_end)
        period_end += frequency

    # If the last generated reset days falls before
    # the maturity, add the maturity
    if period_end != maturity:
        resets.append(maturity)

    # Go through the unadjusted reset dates and adjust if necessary
    # This way if one reset is adjusted, the adjustment
    # is not propagated down the line
    for i, date in enumerate(resets):
        resets[i] = adjust(date, holidays, adjustment)

    # Go through the adjusted resets and generate the full flows
    flows = []
    for i in range(len(resets)-1):
        start = resets[i]
        end = resets[i + 1]
        payment = adjust(end + offset, holidays, adjustment)
        flow = PerformanceFlow(start=start, end=end, payment=payment)
        flows.append(flow)

    return flows

# def generate_interest_rate_flows(
#         start: Date,
#         maturity: Date,
#         frequency: Period,
#         holidays: HolidayBase,
#         adjustment: Adjustment,
#         offset: Period
# ) -> Schedule:
