from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from definitions.day_count import DayCount
from shared.exceptions import ToolkitException

"""
Objectives

rate = InterestRate(0.03)

cash_flow = notional * rate * duration / daycount and take compounding into account

rate = ZeroInterestRate(0.03)

"""


class InvalidInterestRateComparison(ToolkitException):
    pass


class Benchmark(str, Enum):
    """
    Floating interest rates benchmarks.
    """

    ESTER = "ESTER"
    SONIA = "SONIA"


class Compounding(str, Enum):
    """
    Interest rates compounding conventions
    """

    NO_COMPOUNDING = "NoCompounding"  # TODO add simple interest = no compounding
    YEARLY = "Yearly"
    HALF_YEARLY = "HalfYearly"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"
    WEEKLY = "Weekly"
    DAILY = "Daily"
    CONTINUOUS = "Continuous"


@dataclass
class InterestRate:
    """
    Definition of a nominal interest rate.
    """

    rate: Decimal
    compounding: Compounding
    day_count: DayCount

    @property
    def effective(self) -> Decimal:
        # TODO
        match self.compounding:
            case Compounding.YEARLY:
                pass

            case Compounding.MONTHLY:
                return (1 + self.rate / 12) ** 12 - 1

            case Compounding.QUARTERLY:
                return (1 + self.rate / 4) ** 4 - 1

            case Compounding.WEEKLY:
                return (1 + self.rate / 52) ** 52 - 1

            case Compounding.DAILY:
                return (1 + self.rate / 365) ** 365 - 1

            case Compounding.CONTINUOUS:
                return Decimal.exp(self.rate) - 1

    def __eq__(self, other):
        if not isinstance(other, InterestRate):
            raise InvalidInterestRateComparison()

        return self.rate == other.rate and self.compounding == other.compounding

    def __lt__(self, other):
        if not isinstance(other, InterestRate):
            raise InvalidInterestRateComparison()

        return self.effective < other.effective


@dataclass
class FloatingInterestRate:
    benchmark: Benchmark
    spread: float
    compounding: Compounding
    day_count: DayCount
