from dataclasses import dataclass
from datetime import date


@dataclass
class CashDividend:
    ex_date: date
    record_date: date
    amount: float
