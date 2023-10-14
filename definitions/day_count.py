from decimal import Decimal
from enum import Enum

from definitions.date import Date
from definitions.date_range import DateRange


# Some useful definitions
# https://www.isda.org/a/pIJEE/The-Actual-Actual-Day-Count-Fraction-1999.pdf
# https://www.isda.org/a/mIJEE/30-360-2006ISDADefs.xls


class DayCountConvention(str, Enum):
    """
    Day-count conventions.
    30E/360: Eurobond Basis
    30I/360: Bond basis
    """

    ACTUAL_360 = "ACT/360"
    ACTUAL_365 = "ACT/365"
    ACTUAL_ACTUAL_ISDA = "ACT/ACT"  # ACT/ACT ISDA pro rata of daycount in leap year and in non-leap year
    THIRTY_E_360 = "30E/360"
    THIRTY_I_360 = "30I/360"


def compute_year_fraction(start: Date, end: Date, day_count: DayCountConvention) -> Decimal:
    """
    Compute the fraction of year between two dates.
    Used to compute the accrued interests on a wide range of financial instruments.
    """
    calendar_days = (end - start).days

    match day_count:
        case DayCountConvention.THIRTY_E_360:
            """
            This implementation follows the 30E/360 "Eurobond Basis" definition.
            2006 ISDA definitions 4.16g
            """
            # Cap both start and end date to 30
            start.day = min(start.day, 30)
            end.day = min(end.day, 30)

            days = 360 * (end.year - start.year)
            days += 30 * (end.month - start.month)
            days += end.day - start.day
            return Decimal(days) / Decimal(360)

        case DayCountConvention.THIRTY_I_360:
            """
            This implementation follows the 30I/360 "Bond basis" definition.
            2006 ISDA definitions 4.16f
            - D1 is the first calendar day, expressed as a number, of the Calculation Period
              or Compounding Period, unless such number would be 31, in which case D1 will be 30
            - D2 is the calendar day, expressed as a number, immediately following the last day
              included in the Calculation Period or Compounding Period, unless such number would be
              31 and D1 is greater than 29, in which case D2 will be 30
            """
            start.day = min(start.day, 30)
            if start.day > 29:
                end.day = min(end.day, 30)

            days = 360 * (end.year - start.year)
            days += 30 * (end.month - start.month)
            days += end.day - start.day
            return Decimal(days) / Decimal(360)

        case DayCountConvention.ACTUAL_360:
            return Decimal(calendar_days) / Decimal(360)

        case DayCountConvention.ACTUAL_365:
            return Decimal(calendar_days) / Decimal(365)

        case DayCountConvention.ACTUAL_ACTUAL_ISDA:
            """
            This implementation follows the ACT/ACT ISDA definition.
            https://www.isda.org/a/pIJEE/The-Actual-Actual-Day-Count-Fraction-1999.pdf
            """
            leap = sum(1 for x in DateRange(start, end) if x.is_leap)
            non_leap = calendar_days - leap
            return Decimal(leap) / Decimal(366) + Decimal(non_leap) / Decimal(365)
