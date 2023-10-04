from dataclasses import dataclass

from money import Money

from definitions.date import Date


@dataclass
class CashFlow:
    date: Date
    amount: Money
