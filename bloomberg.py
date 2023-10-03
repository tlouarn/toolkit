from dataclasses import dataclass
from enum import Enum

Ticker = str
Exchange = str


class Sector(Enum):
    """
    List of Bloomberg market sectors
    (also known as databases or "yellow keys").
    """

    GOVT = "Govt"
    CORP = "Corp"
    MTGE = "Mtge"
    M_MKT = "M-Mkt"
    MUNI = "Muni"
    PFD = "Pfd"
    EQUITY = "Equity"
    COMDTY = "Comdty"
    INDEX = "Index"
    CURNCY = "Curncy"
    PORT = "Port"


@dataclass
class EquityTicker:
    ticker: Ticker
    exchange: Exchange
    sector: Sector


import blpapi

