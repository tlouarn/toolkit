from enum import Enum

from definitions.currency import Currency
from definitions.date import Date


class Billing(str, Enum):
    MONTHLY = "MONTHLY"


class CollateralType(str, Enum):
    CASH = "CASH"
    NONCASH = "NONCASH"


class CashCollateral:
    type: CollateralType.CASH
    currency: Currency


class CollateralSchedule:
    BONDS = "BONDS"
    EQUITIES = "EQUITIES"


class NonCashCollateral:
    type: CollateralType.NONCASH
    schedule: CollateralSchedule


class StockLoan:
    start: Date
    end: Date
    fee: float
    billing: Billing
    collateral: CashCollateral | NonCashCollateral
    haircut: float
