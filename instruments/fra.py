from dataclasses import dataclass

from definitions.date import Date
from definitions.day_count import DayCount
from definitions.interest_rate import InterestRate


@dataclass
class ForwardRateAgreement:
    fixing: Date
    rate: InterestRate
    day_count: DayCount
