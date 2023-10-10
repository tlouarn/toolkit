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
    ACTUAL_ACTUAL = "ACT/ACT"  # ACT/ACT ISDA pro rata of daycount in leap year and in non-leap year
    THIRTY_E_360 = "30E/360"
    THIRTY_I_360 = "30I/360"


def year_fraction(start_date: Date, end_date: Date, day_count: DayCountConvention) -> Decimal:
    """
    Compute the fraction of year between two dates.
    Used to compute the accrued interests on a wide range of financial instruments.
    """
    calendar_days = (end_date - start_date).days

    match day_count:
        case DayCountConvention.THIRTY_E_360:
            """
            This implementation follows the 30E/360 "Eurobond Basis" definition.
            2006 ISDA definitions 4.16g
            """
            # Cap both start and end date to 30
            start_date.day = min(start_date.day, 30)
            end_date.day = min(end_date.day, 30)

            days = 360 * (end_date.year - start_date.year)
            days += 30 * (end_date.month - start_date.month)
            days += end_date.day - start_date.day
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
            #
            start_date.day = min(start_date.day, 30)
            if start_date.day > 29:
                end_date.day = min(end_date.day, 30)

            days = 360 * (end_date.year - start_date.year)
            days += 30 * (end_date.month - start_date.month)
            days += end_date.day - start_date.day
            return Decimal(days) / Decimal(360)

        case DayCountConvention.ACTUAL_360:
            return Decimal(calendar_days) / Decimal(360)

        case DayCountConvention.ACTUAL_365:
            return Decimal(calendar_days) / Decimal(365)

        case DayCountConvention.ACTUAL_ACTUAL:
            """
            This implementation follows the ACT/ACT ISDA definition.
            https://www.isda.org/a/pIJEE/The-Actual-Actual-Day-Count-Fraction-1999.pdf
            """
            leap = sum(1 for x in DateRange(start_date, end_date) if x.is_leap_year)
            non_leap = calendar_days - leap
            return Decimal(leap) / Decimal(366) + Decimal(non_leap) / Decimal(365)
