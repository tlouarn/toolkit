from __future__ import annotations

import datetime as dt
from enum import Enum
from functools import total_ordering

from dateutil.relativedelta import relativedelta

from definitions.period import Days, Period
from shared.exceptions import ToolkitException


class InvalidDateString(ToolkitException):
    pass


class InvalidOperation(ToolkitException):
    pass


class Weekday(str, Enum):
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"
    SUN = "SUN"


ENDS_OF_MONTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
ENDS_OF_MONTHS_LEAP_YEAR = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


@total_ordering
class Date:
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def __repr__(self) -> str:
        return f"Date({self.year}, {self.month}, {self.day})"

    def __str__(self) -> str:
        return f"{self.year}-{self.month}-{self.day}"

    @classmethod
    def imm(cls, month: int, year: int) -> Date:
        """
        IMM = International Monetary Market
        Instantiate a Date corresponding to the IMM date for a given month and year.
        The IMM date is the third Wednesday of the month .
        """
        date = Date(15, month, year)
        while date.weekday != "WED":
            date += Days(1)
        return date

    @classmethod
    def third_friday(cls, month: int, year: int) -> Date:
        """
        Instantiate a Date corresponding to the third Friday for a given month and year.
        The third Friday of the month is when most European index futures expire.
        """
        date = Date(15, month, year)
        while date.weekday != "FRI":
            date += Days(1)
        return date

    @classmethod
    def today(cls) -> Date:
        """
        Instantiate a Date from today's date.
        """
        date = dt.date.today()
        return Date(date.year, date.month, date.day)

    @classmethod
    def from_date(cls, date: dt.date) -> Date:
        """
        Instantiate a Date from a datetime.date.
        """
        return Date(date.year, date.month, date.day)

    @classmethod
    def parse(cls, string: str) -> Date:
        """
        Instantiate a Date from a string.
        Expected string format is "YYYY-MM-DD".
        """
        if (
            len(string) != 10
            or not string[0:4].isnumeric()
            or not string[5:7].isnumeric()
            or not string[8:10].isnumeric()
        ):
            raise InvalidDateString

        year = int(string[0:4])
        month = int(string[5:7])
        day = int(string[8:10])

        return Date(year, month, day)

    def to_date(self) -> dt.date:
        return dt.date(self.year, self.month, self.day)

    @property
    def weekday(self) -> Weekday:
        date = self.to_date()
        weekday = date.strftime("%a")
        return Weekday(weekday.upper())

    @property
    def is_weekend(self) -> bool:
        return self.weekday in [Weekday.SAT, Weekday.SUN]

    @property
    def is_leap_year(self) -> bool:
        return self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0)

    @property
    def is_eom(self) -> bool:
        """
        Check whether the current Date is the end of month.
        """
        ends_of_months = ENDS_OF_MONTHS_LEAP_YEAR if self.is_leap_year else ENDS_OF_MONTHS
        return self.day == ends_of_months[self.month - 1]

    def get_eom(self) -> Date:
        """
        Return a new Date corresponding to the last day of the current month.
        """
        ends_of_months = ENDS_OF_MONTHS_LEAP_YEAR if self.is_leap_year else ENDS_OF_MONTHS
        last_day = ends_of_months[self.month - 1]
        return Date(self.year, self.month, last_day)

    def __add__(self, other: Period) -> Date:
        """
        Adding a Period to a Date returns a new Date.
        """
        if not isinstance(other, Period):
            raise InvalidOperation("Only a Period can be added to a Date")

        date = dt.date(self.year, self.month, self.day)
        return self._add_delta(date, other)

    def __sub__(self, other: Date | Period) -> Date | Period:
        """
        Subtracting a Date from another Date returns a Period with the number of days in between.
        Subtracting a Period from a Date returns a new Date.
        """
        date = dt.date(self.year, self.month, self.day)

        if isinstance(other, Date):
            other = dt.date(other.year, other.month, other.day)
            days = (date - other).days
            return Days(days)

        elif isinstance(other, Period):
            period = Period(-other.quantity, other.unit)
            return self._add_delta(date, period)

        else:
            raise InvalidOperation(f"Only a Date or a Period can be subtracted from a Date")

    def __hash__(self):
        return hash((self.year, self.month, self.day))

    @staticmethod
    def _add_delta(date: dt.date, period: Period):
        days = period.quantity if period.unit == "D" else 0
        weeks = period.quantity if period.unit == "W" else 0
        months = period.quantity if period.unit == "M" else 0
        years = period.quantity if period.unit == "Y" else 0

        new_date = date + relativedelta(days=days, weeks=weeks, months=months, years=years)
        return Date(new_date.year, new_date.month, new_date.day)

    def __eq__(self, other: Date) -> bool:
        return self.year == other.year and self.month == other.month and self.day == other.day

    def __lt__(self, other) -> bool:
        if self.year != other.year:
            return self.year < other.year

        elif self.month != other.month:
            return self.month < other.month

        elif self.day != other.day:
            return self.day < other.day

        return False
