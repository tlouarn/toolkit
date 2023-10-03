from dataclasses import dataclass

from money import Money

from definitions import Date


@dataclass
class CashFlow:
    date: Date
    amount: Money
