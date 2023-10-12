from decimal import Decimal

from money import Money

from definitions.date import Date
from definitions.day_count import DayCountConvention
from definitions.interest_rate import CompoundingFrequency, InterestRate
from definitions.period import Period
from instruments.deposit import Deposit

INTEREST_RATE = InterestRate(
    rate=Decimal("0.03"), compounding=CompoundingFrequency.YEARLY, day_count=DayCountConvention.ACTUAL_360
)


def test_create_deposit():
    start = Date(2023, 9, 18)
    end = start + Period.parse("1M")
    principal = Money(1_000_000, "EUR")

    # Instantiate the deposit
    deposit = Deposit(start=start, end=end, interest_rate=INTEREST_RATE, principal=principal)

    assert deposit.start == start
    assert deposit.end == end
    assert deposit.interest_rate == INTEREST_RATE
    assert deposit.principal == principal


def test_compute_interests():
    start = Date(2023, 9, 18)
    end = start + Period.parse("1M")
    principal = Money(100_000_000, "EUR")

    # Instantiate the deposit
    deposit = Deposit(start=start, end=end, interest_rate=INTEREST_RATE, principal=principal)

    assert deposit.interests == Money(250_000, "EUR")


def test_compute_interests_annual():
    pass
