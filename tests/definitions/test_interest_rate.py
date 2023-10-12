from decimal import Decimal

from definitions.day_count import DayCountConvention
from definitions.interest_rate import InterestRate
from definitions.frequency import Frequency


def test_instantiate():
    rate = Decimal("0.03")
    convention = DayCountConvention.THIRTY_E_360
    compounding = Frequency.MONTHLY
    interest_rate = InterestRate(rate=rate, convention=convention, compounding=compounding)

    assert interest_rate.rate == rate
    assert interest_rate.convention == convention
    assert interest_rate.compounding == compounding


def test_instantiate_with_defaults():
    rate = Decimal("0.05")
    interest_rate = InterestRate(rate=rate)

    assert interest_rate.rate == rate
    assert interest_rate.convention == DayCountConvention.ACTUAL_360
    assert interest_rate.compounding == Frequency.ANNUAL


def test_compute_annualized_rate():
    rate = Decimal("0.06")

    continuous_rate = InterestRate(rate=rate, compounding=Frequency.CONTINUOUS)
    daily_rate = InterestRate(rate=rate, compounding=Frequency.DAILY)
    weekly_rate = InterestRate(rate=rate, compounding=Frequency.WEEKLY)
    monthly_rate = InterestRate(rate=rate, compounding=Frequency.MONTHLY)
    quarterly_rate = InterestRate(rate=rate, compounding=Frequency.QUARTERLY)
    yearly_rate = InterestRate(rate=rate, compounding=Frequency.ANNUAL)

    assert continuous_rate.effective == Decimal.exp(rate) - 1
    assert daily_rate.effective == (1 + rate / 365) ** 365 - 1
    assert weekly_rate.effective == (1 + rate / 52) ** 52 - 1
    assert monthly_rate.effective == (1 + rate / 12) ** 12 - 1
    assert quarterly_rate.effective == (1 + rate / 4) ** 4 - 1
    assert yearly_rate.effective == rate


def test_compare_interest_rates():
    rate = Decimal("0.06")

    continuous_rate = InterestRate(rate=rate, compounding=Frequency.CONTINUOUS)
    daily_rate = InterestRate(rate=rate, compounding=Frequency.DAILY)
    weekly_rate = InterestRate(rate=rate, compounding=Frequency.WEEKLY)
    monthly_rate = InterestRate(rate=rate, compounding=Frequency.MONTHLY)
    quarterly_rate = InterestRate(rate=rate, compounding=Frequency.QUARTERLY)
    yearly_rate = InterestRate(rate=rate, compounding=Frequency.ANNUAL)

    assert continuous_rate > daily_rate > weekly_rate > monthly_rate > quarterly_rate > yearly_rate
