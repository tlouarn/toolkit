from __future__ import annotations

from enum import Enum
from functools import total_ordering

from shared.exceptions import ToolkitException


# TODO ADD WEEKDAYS
# TODO check sort 7D vs 1W, 12m vs 1Y, 4W vs 1M, 30D vs 1M


class InvalidPeriodUnit(ToolkitException):
    pass


class InvalidPeriodQuantity(ToolkitException):
    pass


class Unit(str, Enum):
    DAY = "D"
    WEEK = "W"
    MONTH = "M"
    YEAR = "Y"


@total_ordering
class Period:
    def __init__(self, quantity: int, unit: Unit):
        self.quantity = quantity
        self.unit = unit

    @classmethod
    def parse(cls, string: str) -> Period:
        """
        Instantiate a Period from a string.
        Examples: "2D", "1W", "3M" or "10Y".
        """
        if not string[:-1].isdigit():
            raise InvalidPeriodQuantity(string)

        if string[-1] not in list(Unit):
            raise InvalidPeriodUnit(string)

        quantity = int(string[:-1])
        unit = Unit(string[-1])

        return Period(quantity=quantity, unit=unit)

    def __str__(self) -> str:
        return f"{self.quantity}{self.unit}"

    def __repr__(self) -> str:
        return f"Period('{self.quantity}{self.unit}')"

    def __eq__(self, other: Period) -> bool:
        if not isinstance(other, Period):
            raise NotImplementedError

        return self.days == other.days

    def __lt__(self, other: Period) -> bool:
        if not isinstance(other, Period):
            raise NotImplementedError

        return self.days < other.days

    def __mul__(self, other: int) -> Period:
        if not isinstance(other, int):
            raise NotImplementedError

        return Period(self.quantity * other, self.unit)

    @property
    def days(self) -> int:
        """
        The average number of days in the Period.
        For example, a month is 365.25 / 12 = 30.42 days on average.
        Used to compare and sort periods.
        """
        match self.unit:
            case "D":
                return self.quantity
            case "W":
                # A week is always 7 days
                return self.quantity * 7
            case "M":
                # A month is on average 30.42 days
                return int(self.quantity * 30.42)
            case "Y":
                # A year is on average 365.25 days
                return int(self.quantity * 365.25)


class Days(Period):
    def __init__(self, quantity: int):
        super().__init__(unit=Unit.DAY, quantity=quantity)


class Months(Period):
    def __init__(self, quantity: int):
        super().__init__(unit=Unit.MONTH, quantity=quantity)


class Weeks(Period):
    def __init__(self, quantity: int):
        super().__init__(unit=Unit.WEEK, quantity=quantity)


class Years(Period):
    def __init__(self, quantity: int):
        super().__init__(unit=Unit.YEAR, quantity=quantity)
