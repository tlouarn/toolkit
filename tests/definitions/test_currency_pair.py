import pytest

from definitions.currency import Currency
from definitions.currency_pair import CurrencyPair, InvalidCurrencyPair


def test_create_currency_pair():
    currency_pair = CurrencyPair(Currency.EUR, Currency.USD)

    assert currency_pair.base == Currency.EUR
    assert currency_pair.quote == Currency.USD


def test_parse_currency_pair():
    currency_pair = CurrencyPair.parse("EURUSD")

    assert currency_pair.base == Currency.EUR
    assert currency_pair.quote == Currency.USD
    assert str(currency_pair) == "EURUSD"


def test_string_representation():
    currency_pair = CurrencyPair(Currency.EUR, Currency.USD)

    assert str(currency_pair) == "EURUSD"


def test_invalid_currency_pair():
    with pytest.raises(InvalidCurrencyPair):
        currency_pair = CurrencyPair.parse("EUR/USD")
