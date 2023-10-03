from dataclasses import dataclass
import datetime as dt

@dataclass
class Option:
    strike: float
    maturity: dt.date



class OptionPricer:

    def __init__(self, option: Option, pricer: Pricer):
        self.option = option
        self.pricer = pricer


    def price(self) -> float:
        return self.pricer.price()