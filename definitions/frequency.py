from enum import Enum


class Frequency(str, Enum):
    """
    Frequencies commonly used in interest rate compounding
    as well as coupon payment.
    """

    NONE = "None"
    ANNUAL = "Annual"
    SEMI_ANNUAL = "SemiAnnual"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"
    WEEKLY = "Weekly"
    DAILY = "Daily"
    CONTINUOUS = "Continuous"
