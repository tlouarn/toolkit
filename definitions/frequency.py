from enum import Enum

from definitions.period import Period


# TODO remove NONE frequency, it's only used for Simple Interest vs CompoundedInterest, ContinuousInterest
# cf https://www.implementingquantlib.com/2013/10/odds-and-ends-interest-rates.html?utm_source=pocket_saves


# Convert payment frequency to period
# TODO embed this within Frequency.to_period() -> return match self.value or not implemented
# less choices than Period so all cases should be close to definition
# also embed a method for compounding periods per year frequency.per_year() -> int


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

    def to_period(self) -> Period:
        match self:
            case Frequency.ANNUAL:
                return Period.parse("1Y")
            case Frequency.SEMI_ANNUAL:
                return Period.parse("6M")
            case Frequency.QUARTERLY:
                return Period.parse("3M")
            case Frequency.MONTHLY:
                return Period.parse("1M")
            case Frequency.WEEKLY:
                return Period.parse("1W")
            case Frequency.DAILY:
                return Period.parse("1D")
            case _:
                raise NotImplementedError

    def per_year(self) -> int:
        raise NotImplementedError
