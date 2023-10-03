from definitions.currency import Currency


def test_create_currency():
    currency = Currency("EUR")

    assert currency == Currency.EUR
