import datetime
from datetime import date

from definitions.dividends import CashDividend
from instruments.forward import Forward
from pricers.forward_pricer import Parameters, SingleStockForwardPricer


def test_stock_forward_pricing_zero_rate_zero_dividend():
    spot = 100
    interest_rate = 0.0
    repo_rate = 0.0
    dividends = []

    pricing_date = date.today()
    maturity = pricing_date + datetime.timedelta(365)

    parameters = Parameters(spot=spot, interest_rate=interest_rate, repo_rate=repo_rate, dividends=dividends)
    forward = Forward(maturity=maturity)
    pricer = SingleStockForwardPricer(forward, parameters)

    value = pricer.price(pricing_date=pricing_date)

    assert value == spot


def test_stock_forward_pricing_without_dividend():
    spot = 100
    interest_rate = 0.05

    pricing_date = date.today()
    maturity = pricing_date + datetime.timedelta(365)

    parameters = Parameters(spot=spot, interest_rate=interest_rate, repo_rate=0.0, dividends=[])
    forward = Forward(maturity=maturity)
    pricer = SingleStockForwardPricer(forward, parameters)

    value = pricer.price(pricing_date=pricing_date)


def test_stock_forward_pricing_with_dividend():
    spot = 100
    interest_rate = 0.05
    repo_rate = 0.0
    dividends = [CashDividend(ex_date=date(2023, 10, 16), record_date=date(2023, 10, 18), amount=3.0)]

    pricing_date = date.today()
    maturity = pricing_date + datetime.timedelta(365)

    parameters = Parameters(spot=spot, interest_rate=interest_rate, repo_rate=repo_rate, dividends=dividends)
    forward = Forward(maturity=maturity)
    pricer = SingleStockForwardPricer(forward, parameters)

    value = pricer.price(pricing_date=pricing_date)
