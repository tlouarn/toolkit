from dataclasses import dataclass


@dataclass
class ForwardRateAgreement:
    fixing: Date
    rate: InterestRate
