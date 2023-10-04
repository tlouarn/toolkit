# import datetime as dt
#
# from definitions.tenor import Tenor
# from instruments.deposit import FixedRateDeposit
#
# RATE_CURVE = {"1D": 0.03, "1W": 0.03, "1M": 0.03, "3M": 0.0315, "6M": 0.032, "9M": 0.032, "1Y": 0.0325}
#
# deposits: list[FixedRateDeposit] = list()
# start = dt.date(2023, 9, 18)
#
# for k, v in RATE_CURVE.items():
#     tenor = k
#     end_date = Tenor.parse(tenor)
#     rate = InterestRate()
#
#     deposit = Deposit(start=start, end_date=end_date, interest_rate=rate)
