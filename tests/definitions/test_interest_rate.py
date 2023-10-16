from decimal import Decimal

from definitions.date import Date
from definitions.day_count import DayCountConvention
from definitions.frequency import Frequency
from definitions.interest_rate import InterestRate


def test_instantiate():
    rate = InterestRate("0.03")
    convention = DayCountConvention.THIRTY_E_360
    compounding = Frequency.MONTHLY
    interest_rate = InterestRate(rate=rate, day_count=convention, compounding=compounding)

    assert interest_rate.rate == rate
    assert interest_rate.day_count == convention
    assert interest_rate.compounding == compounding


def test_instantiate_with_defaults():
    rate = InterestRate("0.05")
    interest_rate = InterestRate(rate=rate)

    assert interest_rate.rate == rate
    assert interest_rate.day_count == DayCountConvention.ACTUAL_360
    assert interest_rate.compounding == Frequency.ANNUAL


def test_compute_annualized_rate():
    rate = InterestRate("0.06")

    continuous_rate = InterestRate(rate=rate, compounding=Frequency.CONTINUOUS)
    daily_rate = InterestRate(rate=rate, compounding=Frequency.DAILY)
    weekly_rate = InterestRate(rate=rate, compounding=Frequency.WEEKLY)
    monthly_rate = InterestRate(rate=rate, compounding=Frequency.MONTHLY)
    quarterly_rate = InterestRate(rate=rate, compounding=Frequency.QUARTERLY)
    yearly_rate = InterestRate(rate=rate, compounding=Frequency.ANNUAL)

    assert continuous_rate.effective == InterestRate.exp(rate) - 1
    assert daily_rate.effective == (1 + rate / 365) ** 365 - 1
    assert weekly_rate.effective == (1 + rate / 52) ** 52 - 1
    assert monthly_rate.effective == (1 + rate / 12) ** 12 - 1
    assert quarterly_rate.effective == (1 + rate / 4) ** 4 - 1
    assert yearly_rate.effective == rate


def test_compare_interest_rates():
    rate = InterestRate("0.06")

    continuous_rate = InterestRate(rate=rate, compounding=Frequency.CONTINUOUS)
    daily_rate = InterestRate(rate=rate, compounding=Frequency.DAILY)
    weekly_rate = InterestRate(rate=rate, compounding=Frequency.WEEKLY)
    monthly_rate = InterestRate(rate=rate, compounding=Frequency.MONTHLY)
    quarterly_rate = InterestRate(rate=rate, compounding=Frequency.QUARTERLY)
    yearly_rate = InterestRate(rate=rate, compounding=Frequency.ANNUAL)

    assert continuous_rate > daily_rate > weekly_rate > monthly_rate > quarterly_rate > yearly_rate


def test_compute_compound_factor_monthly_rate():
    rate = InterestRate("0.12")
    day_count = DayCountConvention.ACTUAL_360
    compounding = Frequency.MONTHLY
    interest_rate = InterestRate(rate=rate, day_count=day_count, compounding=compounding)

    start = Date(2023, 1, 1)
    end = Date(2024, 1, 1)
    compound_factor = interest_rate.to_compound_factor(start=start, end=end)

    assert compound_factor == InterestRate("0.1268")


def test_compute_compound_factor():
    """
    Example taken from
    https://www.deriscope.com/excel/blog/InterestRate.xlsx
    """
    rate = InterestRate("0.04")
    day_count = DayCountConvention.ACTUAL_365
    compounding = Frequency.NONE
    interest_rate = InterestRate(rate=rate, day_count=day_count, compounding=compounding)

    start = Date(2018, 9, 7)
    end = Date(2020, 3, 7)
    compound_factor = interest_rate.to_compound_factor(start=start, end=end)

    assert round(compound_factor, 14) == InterestRate("1.05994520547945")


def test_compute_discount_factor():
    """
    Example taken from
    https://www.deriscope.com/excel/blog/InterestRate.xlsx
    """
    rate = InterestRate("0.04")
    day_count = DayCountConvention.ACTUAL_365
    compounding = Frequency.NONE
    interest_rate = InterestRate(rate=rate, day_count=day_count, compounding=compounding)

    start = Date(2018, 9, 7)
    end = Date(2020, 3, 7)
    discount_factor = interest_rate.to_discount_factor(start=start, end=end)

    assert round(discount_factor, 14) == InterestRate("0.943444995864351")


def test_compute_interests():
    """
    Example taken from
    https://www.rapidtables.com/calc/finance/simple-interest-calculation.html
    :return:
    """
    pass


def test_effective_annual_rate():
    # 5% per annum compounded monthly = 5.116% per annum

    pass


def test_examples_from_option_pricing_formulas():
    """
    Testing the examples from "Option Pricing Formulas" (Haug, 2nd Edition, p. 491)
    """
    day_count = DayCountConvention.ACTUAL_365

    rate_1 = InterestRate(rate=InterestRate("0.08"), day_count=day_count, compounding=Frequency.QUARTERLY)
    rate_2 = InterestRate(rate=InterestRate("0.0792"), day_count=day_count, compounding=Frequency.CONTINUOUS)

    date_1 = Date(2023,1,1)
    date_2 = Date(2024,1,1)

    assert rate_1.to_compound_factor(date_1, date_2) == rate_2.to_compound_factor(date_1, date_2)

    a = 1


def test_other():
    day_count = DayCountConvention.ACTUAL_ACTUAL_ISDA
    rate_1 = InterestRate(rate=InterestRate("0.04"), day_count=day_count, compounding=Frequency.SEMI_ANNUAL)
    print(rate_1.effective)

    rate_2 = InterestRate(rate=InterestRate("0.0404"), day_count=day_count, compounding=Frequency.ANNUAL)
    print(rate_2.effective)

    rate_3 = InterestRate(rate=InterestRate("0.03967068"), day_count=day_count, compounding=Frequency.MONTHLY)
    print(rate_3.effective)