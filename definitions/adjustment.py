from enum import Enum

from holidays import HolidayBase

from definitions.date import Date
from definitions.period import Days


class Adjustment(str, Enum):
    """
    Business day Adjustement conventions
    """

    UNADJUSTED = "Unadjusted"
    PREVIOUS = "Previous"
    MODIFIED_PREVIOUS = "ModifiedPrevious"
    FOLLOWING = "Following"
    MODIFIED_FOLLOWING = "ModifiedFollowing"


def previous(date: Date, holidays: HolidayBase) -> Date:
    """
    Previous business day adjustment
    """
    adjusted_date = date
    while adjusted_date.is_weekend or adjusted_date.to_date() in holidays:
        adjusted_date = adjusted_date - Days(1)
    return adjusted_date


def modified_previous(date: Date, holidays: HolidayBase) -> Date:
    """
    ModifiedPrevious business day adjustment
    """
    adjusted_date = previous(date, holidays)
    if adjusted_date.month == date.month:
        return adjusted_date
    return following(date, holidays)


def following(date: Date, holidays: HolidayBase) -> Date:
    """
    Following business day adjustment
    """
    adjusted_date = date
    while adjusted_date.is_weekend or adjusted_date.to_date() in holidays:
        adjusted_date = adjusted_date + Days(1)
    return adjusted_date


def modified_following(date: Date, holidays: HolidayBase) -> Date:
    """
    ModifiedFollowing business day adjustment
    """
    adjusted_date = following(date, holidays)
    if adjusted_date.month == date.month:
        return adjusted_date
    return previous(date, holidays)


def adjust(date: Date, holidays: HolidayBase, adjustment: Adjustment) -> Date:
    """
    Base method to adjust a date based on given holidays and adjustment method.
    """
    match adjustment:
        case Adjustment.UNADJUSTED:
            return date
        case Adjustment.PREVIOUS:
            return previous(date, holidays)
        case Adjustment.MODIFIED_PREVIOUS:
            return modified_previous(date, holidays)
        case Adjustment.FOLLOWING:
            return following(date, holidays)
        case Adjustment.MODIFIED_FOLLOWING:
            return modified_following(date, holidays)
