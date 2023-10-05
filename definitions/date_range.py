from typing import Iterable

from definitions.date import Date
from definitions.period import Days


class DateRange:
    def __init__(self, start: Date, end: Date):
        self.start = start
        self.end = end

    def __contains__(self, item: Date) -> bool:
        return self.start <= item < self.end

    def __iter__(self) -> list[Date]:
        date = self.start
        while date < self.end:
            yield date
            date += Days(1)
