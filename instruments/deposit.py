from dataclasses import dataclass
from enum import Enum

from money import Money

from definitions.cash_flow import CashFlow
from definitions.date import Date
from definitions.interest_rate import DayCount, InterestRate


class Frequency(str, Enum):
    ANNUAL = "ANNUAL"


@dataclass
class Deposit:
    """
    Implementation of a simple deposit:
        - principal is exchanged at the start date
        - principal + interests are exchanged at the end date
        - computation of interests depends on the InterestRate object
    """

    start: Date
    end: Date
    interest_rate: InterestRate
    principal: Money

    @property
    def days(self) -> int:
        days = self.end - self.start
        return days.days

    @property
    def interests(self) -> Money:
        day_count = 360 if self.interest_rate.day_count == DayCount.ACTUAL_360 else 365  # Todo amend
        interests = self.principal.amount * self.interest_rate.rate * self.days / day_count
        return Money(interests, self.principal.currency)

    @property
    def cash_flows(self) -> list[CashFlow]:
        cash_flows = [
            CashFlow(self.start, self.principal),
            CashFlow(self.end, self.interests),
            CashFlow(self.end, self.principal),
        ]
        return cash_flows


# What this is really is a Deposit Quote
# You can also have Deposit Trades
