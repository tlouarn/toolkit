import math
from dataclasses import dataclass
from datetime import date

from scipy.stats import norm

from instruments.options import Option


@dataclass
class BlackScholesParameters:
    """
    Parameters required by the Black-Scholes model in order to price an option.
    """

    spot: float
    interest_rate: float
    volatility: float
    pricing_date: date


class BlackScholesPricer:
    """
    Implementation of the Black-Scholes pricing model.
    """

    def __init__(self, option: Option, parameters: BlackScholesParameters) -> None:
        self.option = option
        self.parameters = parameters

    @property
    def t(self) -> float:
        """
        Time to maturity expressed in years.
        """
        return (self.option.maturity - self.parameters.pricing_date).days / 365

    @property
    def d1(self) -> float:
        s = self.parameters.spot
        v = self.parameters.volatility
        k = self.option.strike
        r = self.parameters.interest_rate

        return math.log(s / k) + (r + (v ** 2) / 2 * self.t) / (v * math.sqrt(self.t))

    @property
    def d2(self) -> float:
        v = self.parameters.volatility

        return self.d1 - v * math.sqrt(self.t)

    def price(self) -> float:
        return self.price_call() if self.option.type == "CALL" else self.price_put()

    def price_call(self) -> float:
        s = self.parameters.spot
        k = self.option.strike
        r = self.parameters.interest_rate

        return s * norm.cdf(self.d1) - k * math.exp(-r * self.t) * norm.cdf(self.d2)

    def price_put(self) -> float:
        s = self.parameters.spot
        k = self.option.strike
        r = self.parameters.interest_rate

        return k * math.exp(-r * self.t) * norm.cdf(-self.d2) - s * norm.cdf(-self.d1)

    @property
    def delta(self) -> float:
        return norm.cdf(self.d1)
