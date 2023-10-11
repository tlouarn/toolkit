from enum import Enum


class PaymentFrequency(str, Enum):
    """
    Common payment frequencies.
    """

    ANNUAL = "Annual"
    SEMI_ANNUAL = "SemiAnnual"
    QUARTERLY = "Quarterly"
