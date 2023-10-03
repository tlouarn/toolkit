from dataclasses import dataclass

from bloomberg import EquityTicker
from datetime import date
from businessdate import BusinessDate, BusinessPeriod



@dataclass
class Stock:
    isin: str
    name: str
    ticker: EquityTicker


# import QuantLib as ql
#
# date_1 = ql.Date(87895)
# date_2 = ql.Date(2023, 12, 1)
# date_3 = ql.Date("2023-12-01")

bdate = BusinessDate(2023,9,18)

maturity = bdate + BusinessPeriod("1M")

a = 1
