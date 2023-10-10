"""
Interest Rate Swap Pricing
https://www.r-bloggers.com/2021/07/interest-rate-swap-pricing-using-r-code/
"""
from decimal import Decimal

from definitions.date import Date
from definitions.day_count import DayCountConvention, year_fraction
from definitions.interest_rate import InterestRate

valuation = Date(2021, 7, 2)
maturity = Date(2021, 10, 4)

market_rate = InterestRate(Decimal("0.0014575"))

fraction = year_fraction(valuation, maturity, DayCountConvention.THIRTY_E_360)

# class PaymentFrequency:
#     ANNUAL
#     SEMI_ANNUAL

# class DayCount:

a = 1

dates = [
    Date.parse("2021-10-04"),
    Date.parse("2021-12-15"),
    Date.parse("2022-03-16"),
    Date.parse("2022-06-15"),
    Date.parse("2022-09-21"),
    Date.parse("2022-12-21"),
    Date.parse("2023-03-15"),
    Date.parse("2023-07-03"),
    Date.parse("2024-07-02"),
    Date.parse("2025-07-02"),
    Date.parse("2026-07-02"),
    Date.parse("2027-07-02"),
    Date.parse("2028-07-03"),
    Date.parse("2029-07-02"),
    Date.parse("2030-07-02"),
    Date.parse("2031-07-02"),
    Date.parse("2032-07-02"),
    Date.parse("2033-07-05"),
    Date.parse("2036-07-02"),
    Date.parse("2041-07-02"),
    Date.parse("2046-07-02"),
    Date.parse("2051-07-03"),
    Date.parse("2061-07-05"),
    Date.parse("2071-07-02"),
]

rates = [
    Decimal("0.00147746193495074"),
    Decimal("0.00144337757980778"),
    Decimal("0.00166389741542625"),
    Decimal("0.00175294804717070"),
    Decimal("0.00196071374597585"),
    Decimal("0.00224582504806747"),
    Decimal("0.00264462838911974"),
    Decimal("0.00328408008984121"),
    Decimal("0.00571530169527018"),
    Decimal("0.00795496282359075"),
    Decimal("0.00970003866673104"),
    Decimal("0.01113416387898720"),
    Decimal("0.01229010329346910"),
    Decimal("0.01320660291639990"),
    Decimal("0.01396222829363160"),
    Decimal("0.01461391064905110"),
    Decimal("0.01518876914165160"),
    Decimal("0.01567359620429550"),
    Decimal("0.01673867348140660"),
    Decimal("0.01771539830734830"),
    Decimal("0.01798302077085120"),
    Decimal("0.01801516858533200"),
    Decimal("0.01707008589009480"),
    Decimal("0.01580574448899780"),
]


# Swap Schedule
