# https://quant.stackexchange.com/questions/53904/monotonic-cubic-spline-interpolation-quantlib-python
from decimal import Decimal

import QuantLib as ql

from definitions.date import Date
from definitions.discount_curve import DiscountCurve
from definitions.discount_factor import DiscountFactor

ql.Settings.instance().evaluationDate = ql.Date(8, 5, 2020)

market_data = [
    ("DEPOSIT", "6M", -0.114),
    ("FRA", "6M", -0.252),
    ("FRA", "12M", -0.306),
    ("SWAP", "2Y", -0.325),
    ("SWAP", "3Y", -0.347),
]

helpers = ql.RateHelperVector()
index = ql.Euribor6M()
for instrument, tenor, rate in market_data:
    rate /= 100
    if instrument == "DEPOSIT":
        helpers.append(ql.DepositRateHelper(rate, index))
    if instrument == "FRA":
        monthsToStart = ql.Period(tenor).length()
        helpers.append(ql.FraRateHelper(rate, monthsToStart, index))
    if instrument == "SWAP":
        helpers.append(
            ql.SwapRateHelper(
                rate, ql.Period(tenor), ql.TARGET(), ql.Annual, ql.Following, ql.Thirty360(ql.Thirty360.USA), index
            )
        )

params = [2, ql.TARGET(), helpers, ql.ActualActual(ql.ActualActual.ISDA)]
curves = {
    "PiecewiseFlatForward": ql.PiecewiseFlatForward(*params),
    "LogLinearDiscount": ql.PiecewiseLogLinearDiscount(*params),
    "LogCubicDiscount": ql.PiecewiseLogCubicDiscount(*params),
    "LinearZero": ql.PiecewiseLinearZero(*params),
    "CubicZero": ql.PiecewiseCubicZero(*params),
    "LinearForward": ql.PiecewiseLinearForward(*params),
    "SplineCubicDiscount": ql.PiecewiseSplineCubicDiscount(*params),
}

import pandas as pd

df = pd.DataFrame(index=[row[0] for row in curves["LogLinearDiscount"].nodes()])
for curve in curves:
    dfs = [curves[curve].discount(idx) for idx in df.index]
    df[curve] = dfs

new_df = pd.DataFrame(index=[idx + ql.Period("15d") for idx in df.index])
for curve in curves:
    curves[curve].enableExtrapolation()
    dfs = [curves[curve].discount(idx) for idx in new_df.index]
    new_df[curve] = dfs
date = ql.Date(5, 12, 2020)

"""
Recreating the example with toolkit
"""

discount_factors = []
for k, v in df["LogLinearDiscount"].to_dict().items():
    discount_factor = DiscountFactor(
        start=Date(2020,5,8), end=Date(k.year(), k.month(), k.dayOfMonth()), factor=Decimal(v)
    )
    discount_factors.append(discount_factor)

discount_curve = DiscountCurve(discount_factors)

interpolations = []
interp_dates = [Date(2020,5,27), Date(2020,11,27), Date(2021,5,27), Date(2021,11,27), Date(2022,5,27), Date(2023,5,27)]
for date in interp_dates:
    print(discount_curve.get(date))




date_1 = Date(2020, 5, 12)
date_2 = Date(2020, 11, 12)

df_1 = Decimal(1)
df_2 = Decimal(1.000583)

date_i = Date(2020, 5, 27)

weight_1 = Decimal((date_2 - date_i).days) / Decimal((date_2 - date_1).days)
weight_2 = Decimal((date_i - date_1).days) / Decimal((date_2 - date_1).days)

df_i = weight_1 * Decimal.ln(df_1) + weight_2 * Decimal.ln(df_2)
df_i = Decimal.exp(df_i)


a = 1
