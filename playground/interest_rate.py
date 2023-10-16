from decimal import Decimal

from definitions.date import Date
from definitions.frequency import Frequency


class InterestRate(Decimal):
    def __init__(self, rate: str | int | Decimal):
        if not isinstance(rate, str) and not isinstance(rate, int) and not isinstance(rate, Decimal):
            raise ValueError()
        super().__init__()


class DiscountFactor(Decimal):
    pass


def to_continuous(interest_rate: InterestRate, compounding: Frequency) -> InterestRate:
    pass


rate = InterestRate("0.01")
rate = InterestRate(1)
rate = InterestRate(Decimal("0.01"))

rate = InterestRate.simple("0.01")
rate = InterestRate.compounded("0.01", "Annual")
rate = InterestRate.continuous("0.01").to_simple()

nominal_rate = InterestRate.nominal
effective_rate = InterestRate.effective
type = InterestRate.type
day_count = InterestRate.day_count


class InterestRate:
    def __init__(self, nominal: Decimal | str | int) -> None:
        # BASE CLASS FOR INTEREST RATES
        # Defined as a rate with associated category (Simple | Compounded | Continuous)
        # Defined with associated DayCountConvention
        # Complete interoperability with DiscountFactor and CompoundFactor between 2 dates
        # Different constructors depending on how the interest rate is initially defined
        # Conversions between types of interest rates
        # Computation of DiscountFactor and CompoundFactor

        self.nominal = nominal  # Nominal interest rate
        pass

    @classmethod
    def simple(cls, rate: Decimal) -> InterestRate:
        pass

    @classmethod
    def compounded(cls, rate: Decimal, frequency: Frequency) -> InterestRate:
        pass

    @classmethod
    def continuous(cls, rate: Decimal) -> InterestRate:
        pass

    def to_compounded(self, frequency: Frequency) -> InterestRate:
        pass

    def to_simple(self) -> InterestRate:
        pass

    def to_continuous(self) -> InterestRate:
        pass

    def to_discount_factor(self, start: Date, end: Date) -> Decimal:
        pass

    def to_compound_factor(self, start: Date, end: Date) -> Decimal:
        pass


if __name__ == "__main__":
    interest_rate = InterestRate.simple(Decimal("0.05")).to_continuous()
    # interest_rate_2 = InterestRate(0.05)
    print(interest_rate)

    assert isinstance(interest_rate, Decimal)
    assert isinstance(interest_rate, InterestRate)
