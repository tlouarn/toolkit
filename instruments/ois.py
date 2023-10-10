# From QuantLib
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Literal

import QuantLib as ql
from holidays import HolidayBase, financial_holidays

from definitions.adjustment import Adjustment, adjust
from definitions.date import Date
from definitions.day_count import DayCount
from definitions.interest_rate import Compounding
from definitions.period import Period

swapType = ql.OvernightIndexedSwap.Receiver
nominal = 100
schedule = ql.MakeSchedule(ql.Date(15, 6, 2020), ql.Date(15, 6, 2021), ql.Period("1Y"), calendar=ql.TARGET())
fixedRate = 0.01
fixedDC = ql.Actual360()
overnightIndex = ql.Eonia()
ois_swap = ql.OvernightIndexedSwap(swapType, nominal, schedule, fixedRate, fixedDC, overnightIndex)

a = 1


# https://www.clarusft.com/ois-swap-nuances/
# http://mikejuniperhill.blogspot.com/2015/07/pricing-bloomberg-swap-manager.html

class Way:
    PAYER = "PAYER"
    RECEIVER = "RECEIVER"


@dataclass
class OvernightIndex:
    name: str
    day_count: DayCount
    lag: Period


ESTER = OvernightIndex("ESTER", DayCount.ACTUAL_360, 0)


class OvernightIndex(str, Enum):
    ESTER = "ESTER"
    SONIA = "SONIA"


@dataclass
class Benchmark:
    name: str
    fixing: Date
    publication: Date
    start: Date
    end: Date
    value: Decimal


payment_frequencies = Literal["1M", "3M", "1T"]  # 1T = "TERM" = bullet payment = only one payment at maturity


# Fixed-floating swap
# Floating rate
# Swap maturity
# Reset frequency
# Compounding convention
# Fixed rate price


class FixedLeg:
    payment_frequency: Period
    day_count: DayCount
    compounding: Compounding


class FloatingLeg:
    payment_frequency: Period
    day_count: DayCount
    compounding: Compounding


class OIS:
    fixed_leg: FixedLeg
    floating_leg: FloatingLeg


# TODO an "adjuster" object already filled with the HolidayBase and the AdjustmentMethod
# adjuster = Adjuster(holidays=financial_holidays("ECB"), method=AdjustmentMethod.ModifiedFollowing)


def make_ois_schedule(
        start_date: Date, tenor: Period, step: Period, holidays: HolidayBase, adjustment: Adjustment
) -> list[Date]:
    schedule = []

    # ASSUMES FRONT_STUB swap

    # Compute swap maturity
    maturity = start_date + tenor

    # Adjust swap maturity
    maturity = adjust(maturity, holidays, adjustment)
    schedule.append(maturity)

    # Check if maturity is > step
    if maturity < start_date + step:
        return schedule

    # Compute unadjusted intermediary payment dates
    date = maturity - step
    while date > start_date:
        schedule.append(date)
        date = date - step

    # Adjust intermediary payment dates
    schedule = [adjust(date, holidays, adjustment) for date in schedule]

    return schedule


if __name__ == "__main__":
    start_date = Date.today()
    tenor = Period.parse("1Y")
    step = Period.parse("1M")
    holidays = financial_holidays("ECB")
    adjustment = Adjustment.MODIFIED_FOLLOWING
    schedule = make_ois_schedule(start_date, tenor, step, holidays, adjustment)

    a = 1



# Fitting to a step curve
# ECB meetings effective dates
