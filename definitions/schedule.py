from dataclasses import dataclass
from enum import Enum

from holidays import HolidayBase

from definitions.adjustment import Adjustment, adjust
from definitions.date import Date
from definitions.period import Period


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


@dataclass
class EquityLinkedSwapSchedule:
    performance: Schedule
    interest_rate: Schedule
    dividend_resets: Schedule


def generate_performance_resets(
    start: Date,
    maturity: Date,
    frequency: Period,
    holidays: HolidayBase,
    adjustment: Adjustment,
    offset: Period,
) -> list[PerformanceFlow]:
    """
    TODO: Add Stub.FRONT or Stub.BACK
    """

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

    # Go through the resets and adjust if necessary
    # This way if one reset is adjusted, the adjustment
    # is not propagated down the line
    for i, date in enumerate(resets):
        resets[i] = adjust(date, holidays, adjustment)

    # Go through the adjusted resets and generate the flows
    flows = []
    for i in range(len(resets)):
        start = resets[i]
        end = resets[i + 1]
        payment = adjust(start + offset, holidays, adjustment)
        flow = PerformanceFlow(start=start, end=end, payment=payment)
        flows.append(flow)

    return flows
