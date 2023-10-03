from datetime import date

from instruments.options import Option
from pricers.black_scholes import BlackScholesParameters, BlackScholesPricer


def test_price_call_option():
    """
    Pricing of a DEC23 300 MSFT option as of 27 SEP 2023.
    """
    option = Option(type="CALL", strike=300, maturity=date(2023, 12, 15))
    parameters = BlackScholesParameters(spot=312, interest_rate=0.05, volatility=0.3, pricing_date=date(2023, 9, 27))
    pricer = BlackScholesPricer(option, parameters)
    value = pricer.price()

    assert round(value, 2) == 25.61


def test_price_zero_volatility_option():
    option = Option(type="CALL", strike=300, maturity=date(2023, 12, 15))
    parameters = BlackScholesParameters(spot=250, interest_rate=0, volatility=0, pricing_date=date(2023, 9, 18))
    pricer = BlackScholesPricer(option, parameters)
    value = pricer.price()

    assert value == 0


def test_delta_option():
    option = Option(type="CALL", strike=100, maturity=date(2023, 12, 15))

    spot_1 = 100
    spot_2 = 100.01

    parameters_1 = BlackScholesParameters(spot=spot_1, interest_rate=0.05, volatility=0.3, pricing_date=date(2023, 9, 18))
    parameters_2 = BlackScholesParameters(spot=spot_2, interest_rate=0.05, volatility=0.3, pricing_date=date(2023, 9, 18))

    value_1 = BlackScholesPricer(option, parameters_1).price()
    value_2 = BlackScholesPricer(option, parameters_2).price()

    delta = (value_2 - value_1) / (spot_2 - spot_1)

    assert delta == BlackScholesPricer(option, parameters_1).delta

    print(delta)
