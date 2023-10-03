import datetime as dt
from dataclasses import dataclass

from money import Money

from definitions.cash_flow import CashFlow
from definitions.date import Date

from definitions.interest_rate import FixedInterestRate


@dataclass
class Deposit:
    start: Date
    end: Date
    interest_rate: FixedInterestRate
    notional: Money
    compounding: Compounding

    @property
    def days(self) -> int:
        return self.end - self.start

    @property
    def cash_flows(self) -> list[CashFlow]:

        return [
            CashFlow(self.start, self.notional),
            CashFlow(self.end, self.notional * (1 + self.interest_rate.rate))
        ]

@dataclass
class FixedRateDeposit:
    start: dt.date
    end: dt.date
    interest_rate: FixedInterestRate


# What this is really is a Deposit Quote
# You can also have Deposit Trades


@dataclass
class DepositTrade:
    td: date
    vd: date
    maturity: date
    notional: float
    rate: float
    book: str
    counterpart: str
