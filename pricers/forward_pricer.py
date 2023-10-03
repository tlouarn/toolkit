import math
from dataclasses import dataclass
from datetime import date

from instruments.forward import Forward


@dataclass
class CashDividend:
    ex_date: date
    record_date: date
    amount: float


DividendCurve = list[CashDividend]

# TODO forward with dividends in different currency


@dataclass
class Parameters:
    spot: float
    interest_rate: float
    repo_rate: float
    dividends: DividendCurve  # Check that all dividends are in the future


"""
Simple constant rate forward pricer.
"""


class SingleStockForwardPricer:
    def __init__(self, forward: Forward, parameters: Parameters):
        self.forward = forward
        self.parameters = parameters

    def price(self, pricing_date: date) -> float:
        spot = self.parameters.spot
        rate = self.parameters.interest_rate
        repo = self.parameters.repo_rate
        time = (self.forward.maturity - pricing_date).days / 365.0

        # Discount the dividends
        discounted_dividends = 0
        for dividend in self.parameters.dividends:
            time = (dividend.ex_date - pricing_date).days / 365.0
            discounted_dividend = dividend.amount / math.exp(rate * time)
            discounted_dividends += discounted_dividend

        return (spot - discounted_dividends) * math.exp((rate - repo) * time)
