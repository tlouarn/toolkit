from enum import Enum

from holidays import HolidayBase

from definitions.date import Date
from definitions.period import Days


class BusinessDayConvention(str, Enum):
    """
    Business day adjustment conventions.
    Usage:
    - convention = BusinessDayConvention("ModifiedFollowing")
    - convention = BusinessDayConvention.MODIFIED_FOLLOWING
    """

    UNADJUSTED = "Unadjusted"
    PREVIOUS = "Previous"
    MODIFIED_PREVIOUS = "ModifiedPrevious"
    FOLLOWING = "Following"
    MODIFIED_FOLLOWING = "ModifiedFollowing"


def previous(date: Date, holidays: HolidayBase) -> Date:
    """
    Previous business day adjustment.
    """
    adjusted_date = date
    while adjusted_date.is_weekend or adjusted_date.to_date() in holidays:
        adjusted_date = adjusted_date - Days(1)
    return adjusted_date


def modified_previous(date: Date, holidays: HolidayBase) -> Date:
    """
    ModifiedPrevious business day adjustment.
    """
    adjusted_date = previous(date, holidays)
    if adjusted_date.month == date.month:
        return adjusted_date
    return following(date, holidays)


def following(date: Date, holidays: HolidayBase) -> Date:
    """
    Following business day adjustment.
    """
    adjusted_date = date
    while adjusted_date.is_weekend or adjusted_date.to_date() in holidays:
        adjusted_date = adjusted_date + Days(1)
    return adjusted_date


def modified_following(date: Date, holidays: HolidayBase) -> Date:
    """
    ModifiedFollowing business day adjustment.
    """
    adjusted_date = following(date, holidays)
    if adjusted_date.month == date.month:
        return adjusted_date
    return previous(date, holidays)


def adjust_date(date: Date, holidays: HolidayBase, adjustment: BusinessDayConvention) -> Date:
    """
    Base method to adjust a date based on given holidays and a business day convention.
    """
    match adjustment:
        case BusinessDayConvention.UNADJUSTED:
            return date
        case BusinessDayConvention.PREVIOUS:
            return previous(date, holidays)
        case BusinessDayConvention.MODIFIED_PREVIOUS:
            return modified_previous(date, holidays)
        case BusinessDayConvention.FOLLOWING:
            return following(date, holidays)
        case BusinessDayConvention.MODIFIED_FOLLOWING:
            return modified_following(date, holidays)
