from enum import Enum

from definitions.date import Date


class Calendar(str, Enum):
    TARGET = "TARGET"




class Holidays:

    def __init__(self, calendar: Calendar):
        self.calendar = calendar

    def get_holidays(self, year: int) -> list[Date]:
        pass