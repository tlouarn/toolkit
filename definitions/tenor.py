from __future__ import annotations

from enum import Enum
from functools import total_ordering


class InvalidTenorUnit(Exception):
    pass


class InvalidTenorQuantity(Exception):
    pass


class Unit(str, Enum):
    DAY = "D"
    WEEK = "W"
    MONTH = "M"
    YEAR = "Y"


@total_ordering
class Tenor:
    def __init__(self, quantity: int, unit: Unit):
        self.quantity = quantity
        self.unit = unit

    @classmethod
    def parse(cls, string: str) -> Tenor:
        """
        Instantiate a Tenor object from a string e.g. "1M".
        """
        if not string[:-1].isnumeric():
            raise InvalidTenorQuantity(string)

        if string[-1] not in list(Unit):
            raise InvalidTenorUnit(string)

        quantity = int(string[:-1])
        unit = Unit(string[-1])

        return Tenor(quantity=quantity, unit=unit)

    def __str__(self) -> str:
        return f"{self.quantity}{self.unit}"

    def __repr__(self) -> str:
        return f"Tenor('{self.quantity}{self.unit}')"

    def __eq__(self, other: Tenor) -> bool:
        if not isinstance(other, Tenor):
            raise NotImplementedError

        return self.days == other.days

    def __lt__(self, other: Tenor) -> bool:
        if not isinstance(other, Tenor):
            raise NotImplementedError

        return self.days < other.days

    @property
    def days(self) -> int:
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


class Days(Tenor):
    def __init__(self, quantity: int):
        super().__init__(unit=Unit.DAY, quantity=quantity)


class Months(Tenor):
    def __init__(self, quantity: int):
        super().__init__(unit=Unit.MONTH, quantity=quantity)
