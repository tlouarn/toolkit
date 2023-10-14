from decimal import Decimal
from datetime import date as Date

class InterestRate(Decimal):
    def __init__(self, rate: str | int | Decimal):
        if not isinstance(rate, str) and not isinstance(rate, int) and not isinstance(rate, Decimal):
            raise ValueError()
        super().__init__()

class DiscountFactor(Decimal):
    pass


def to_continuous(interest_rate: InterestRate, compounding: Frequency) -> InterestRate:
    pass




if __name__ == "__main__":
    interest_rate = InterestRate("0.05")
    # interest_rate_2 = InterestRate(0.05)
    print(interest_rate)

    assert isinstance(interest_rate, Decimal)
    assert isinstance(interest_rate, InterestRate)
