from definitions.currency import Currency


def test_instantiate_currency():
    currency = Currency("EUR")

    assert currency == "EUR"
    assert currency == Currency.EUR

