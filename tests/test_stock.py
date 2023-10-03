from bloomberg import EquityTicker
from stock import Stock


def test_create_stock():
    isin = "US5949181045"
    name = "Microsoft Corp."
    ticker = EquityTicker.from_string("MSFT US Equity")
    stock = Stock(isin=isin, name=name, ticker=ticker)

    assert stock.isin == isin
    assert stock.name == name
    assert stock.ticker == ticker
