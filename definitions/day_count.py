from decimal import Decimal
from enum import Enum

from definitions.date import Date
from definitions.date_range import DateRange


# Some useful definitions
# https://www.isda.org/a/pIJEE/The-Actual-Actual-Day-Count-Fraction-1999.pdf


class DayCount(str, Enum):
    """
    Day count conventions.
    """

    ACT_360 = "ACT/360"
    ACT_365 = "ACT/365"
    ACT_ACT = "ACT/ACT"  # ACT/ACT ISDA pro rata of daycount in leap year and in non-leap year


def year_fraction(start_date: Date, end_date: Date, day_count: DayCount) -> Decimal:
    """
    Compute the year fraction between two dates.
    Used to compute the accrued interests on a wide range of financial instruments.
    """
    calendar_days = (end_date - start_date).days

    match day_count:
        case DayCount.ACT_360:
            return Decimal(calendar_days / 360)

        case DayCount.ACT_365:
            return Decimal(calendar_days / 365)

        case DayCount.ACT_ACT:
            """
            This implementation follows the ACT/ACT ISDA definition.
            """
            leap = sum(1 for x in DateRange(start_date, end_date) if x.is_leap_year)
            non_leap = calendar_days - leap
            return Decimal(leap / 366) + Decimal(non_leap / 365)
