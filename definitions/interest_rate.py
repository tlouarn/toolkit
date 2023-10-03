from dataclasses import dataclass
from enum import Enum


"""
Objectives

rate = InterestRate(0.03)

cash_flow = notional * rate * duration / daycount and take compounding into account

rate = ZeroInterestRate(0.03)

"""


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

    NO_COMPOUNDING = "NoCompounding"
    ANNUAL = "Annual"
    SEMI_ANNUAL = "SemiAnnual"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"
    WEEKLY = "Weekly"
    DAILY = "Daily"
    CONTINUOUS = "Continuous"


class DayCount(str, Enum):
    """
    Day count conventions.
    """

    ACT_360 = "ACT/360"
    ACT_365 = "ACT/365"


@dataclass
class InterestRate:
    rate: float
    compounding: Compounding
    day_count: DayCount


@dataclass
class FloatingInterestRate:
    benchmark: Benchmark
    spread: float
    compounding: Compounding
    day_count: DayCount
