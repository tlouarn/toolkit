from dataclasses import dataclass
from decimal import Decimal
import datetime as dt
from stock import Stock


@dataclass
class IndexWeight:
    instrument: Stock
    weight: Decimal


@dataclass
class IndexComposition:
    divisor: Decimal
    weights: list[IndexWeight]


@dataclass
class Price:
    stock: Stock
    price: Decimal
    date: dt.date


def compute_index(composition: IndexComposition, prices: list[Price]):
    # Check that all index stocks have a price


    # Compute index
    pass
