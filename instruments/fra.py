from dataclasses import dataclass

from definitions.date import Date
from definitions.day_count import DayCountConvention
from definitions.interest_rate import Decimal


@dataclass
class ForwardRateAgreement:
    fixing: Date
    rate: Decimal
    day_count: DayCountConvention
