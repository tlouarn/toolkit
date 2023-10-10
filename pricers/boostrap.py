"""
Rate curve bootstrapping from ESTER swap rates.
"""

class EsterSwap(OIS):

    def __init__(self, start_date: Date, tenor: Period, price: Decimal)

        # start_date
        # tenor
        # generate schedule
        # generate paydates
        # apply rate convention
        # create fixed rate (the price)

FixedLeg: Annual, ACT/360
FloatingLeg: Annual, ACT/360


ester_1w = EsterSwap(start_date, end_date, rate: Decimal)