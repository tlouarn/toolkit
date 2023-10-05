from decimal import Decimal
from enum import Enum

from definitions.date import Date
from definitions.date_range import DateRange


# Some useful definitions
# https://www.isda.org/a/pIJEE/The-Actual-Actual-Day-Count-Fraction-1999.pdf


class DayCount(str, Enum):
    """
    Day-count conventions.
    """

    ACTUAL_360 = "ACT/360"
    ACTUAL_365 = "ACT/365"
    ACTUAL_ACTUAL = "ACT/ACT"  # ACT/ACT ISDA pro rata of daycount in leap year and in non-leap year
    THIRTY_360 = "30E/360"  # 30E/360 "EUROBOND BASIS"


def year_fraction(start_date: Date, end_date: Date, day_count: DayCount) -> Decimal:
    """
    Compute the year fraction between two dates.
    Used to compute the accrued interests on a wide range of financial instruments.
    """
    calendar_days = (end_date - start_date).days

    match day_count:
        case DayCount.THIRTY_360:
            """
            This implementation follows the 30E/360 "Eurobond Basis" definition.
            """
            # Cap both start and end date to 30
            start_date.day = min(start_date.day, 30)
            end_date.day = min(end_date.day, 30)

            days = 360 * (end_date.year - start_date.year)
            days += 30 * (end_date.month - start_date.month)
            days += end_date.day - start_date.day
            return Decimal(days) / Decimal(360)

        case DayCount.ACTUAL_360:
            return Decimal(calendar_days) / Decimal(360)

        case DayCount.ACTUAL_365:
            return Decimal(calendar_days) / Decimal(365)

        case DayCount.ACTUAL_ACTUAL:
            """
            This implementation follows the ACT/ACT ISDA definition.
            https://www.isda.org/a/pIJEE/The-Actual-Actual-Day-Count-Fraction-1999.pdf
            """
            leap = sum(1 for x in DateRange(start_date, end_date) if x.is_leap_year)
            non_leap = calendar_days - leap
            return Decimal(leap) / Decimal(366) + Decimal(non_leap) / Decimal(365)
