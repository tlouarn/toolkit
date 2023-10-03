from dataclasses import dataclass
from decimal import Decimal

from pendulum import Date


@dataclass
class DateRange:
    start: Date
    end: Date

    def __contains__(self, date: Date) -> bool:
        return self.start <= date <= self.end


@dataclass
class FrenchScrip:
    """
    Can be implemented as a floating-strike Asian option.
    """

    ex_date: Date
    record_date: Date
    election_period: DateRange
    striking_period: DateRange  # also named determination_period
    discount: Decimal


if __name__ == "__main__":
    start = Date(2020, 4, 30)
    end = Date(2020, 5, 28)
    striking_period = DateRange(start=start, end=end)

    print(Date(2023, 5, 5) in striking_period)


"""
https://stackoverflow.com/questions/993358/creating-a-range-of-dates-in-python?noredirect=1&lq=1

from datetime import date, timedelta, datetime

class DateRange:
    def __init__(self, start, end, step=timedelta(1)):
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self):
        start = self.start
        step = self.step
        end = self.end

        n = int((end - start) / step)
        d = start

        for _ in range(n):
            yield d
            d += step

    def __contains__(self, value):
        return (
            (self.start <= value < self.end) and 
            ((value - self.start) % self.step == timedelta(0))
        )
"""
