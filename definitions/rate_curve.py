from definitions.date import Date
from definitions.interest_rate import Decimal


class InterestRateCurve:
    def __init__(self, dates: list[Date], interest_rates: list[Decimal]) -> None:
        self.curve = {k: v for k, v in zip(dates, interest_rates)}

    def get_spot(self, date: Date) -> Decimal:
        pass

    def get_forward(self, from_date: Date, to_date: Date) -> Decimal:
        pass
