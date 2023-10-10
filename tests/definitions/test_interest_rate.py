from decimal import Decimal

from definitions.interest_rate import Compounding, InterestRate


def test_instantiate_interest_rate():
    rate = Decimal("0.03")
    compounding = Compounding.YEARLY
    interest_rate = InterestRate(rate=rate, compounding=compounding)

    assert interest_rate.rate == rate
    assert interest_rate.compounding == compounding


def test_compute_annualized_rate():
    rate = Decimal("0.06")

    continuous_rate = InterestRate(rate=rate, compounding=Compounding.CONTINUOUS)
    daily_rate = InterestRate(rate=rate, compounding=Compounding.DAILY)
    weekly_rate = InterestRate(rate=rate, compounding=Compounding.WEEKLY)
    monthly_rate = InterestRate(rate=rate, compounding=Compounding.MONTHLY)
    quarterly_rate = InterestRate(rate=rate, compounding=Compounding.QUARTERLY)
    yearly_rate = InterestRate(rate=rate, compounding=Compounding.YEARLY)

    assert continuous_rate.annualized == Decimal.exp(rate) - 1
    assert daily_rate.annualized == (1 + rate / 365) ** 365 - 1
    assert weekly_rate.annualized == (1 + rate / 52) ** 52 - 1
    assert monthly_rate.annualized == (1 + rate / 12) ** 12 - 1
    assert quarterly_rate.annualized == (1 + rate / 4) ** 4 - 1
    assert yearly_rate.annualized == rate


def test_compare_interest_rates():
    rate = Decimal("0.06")

    continuous_rate = InterestRate(rate=rate, compounding=Compounding.CONTINUOUS)
    daily_rate = InterestRate(rate=rate, compounding=Compounding.DAILY)
    weekly_rate = InterestRate(rate=rate, compounding=Compounding.WEEKLY)
    monthly_rate = InterestRate(rate=rate, compounding=Compounding.MONTHLY)
    quarterly_rate = InterestRate(rate=rate, compounding=Compounding.QUARTERLY)
    yearly_rate = InterestRate(rate=rate, compounding=Compounding.YEARLY)

    assert continuous_rate > daily_rate > weekly_rate > monthly_rate > quarterly_rate > yearly_rate

