from __future__ import annotations

from dataclasses import dataclass
from datetime import date



@dataclass
class ForexForward:
    pair: Pair
    maturity: date


@dataclass
class Parameters:
    interest_rate_


class ForexForwardPricer:
    def __init__(self, forward: ForexForward, parameters: Parameters):
        pass
