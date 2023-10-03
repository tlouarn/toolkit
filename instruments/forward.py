from dataclasses import dataclass
from datetime import date


@dataclass
class Forward:
    maturity: date
