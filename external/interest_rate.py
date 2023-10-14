"""
Example taken from
https://www.deriscope.com/excel/blog/InterestRate.xlsx

Issues:
- the library uses floats, so we need math.isclose() to compare results
- `impliedRate` is a method of `InterestRate` but does not use any of its attributes
"""
import math

import QuantLib as ql

# Create InterestRate object
rate = 0.04
day_counter = ql.Actual365Fixed()
compounding = ql.Simple
interest_rate = ql.InterestRate(rate, day_counter, compounding, 0)

# Define two dates
start = ql.Date(7, 9, 2018)
end = ql.Date(7, 3, 2020)

# Compute the CompoundFactor
compound_factor = interest_rate.compoundFactor(start, end)
assert math.isclose(compound_factor, 1.05994520547945)

# Compute the ImpliedRate
implied_rate = interest_rate.impliedRate(compound_factor, ql.Actual365Fixed(), ql.Simple, ql.Annual, start, end)
assert math.isclose(implied_rate.rate(), rate)

# Compute the DiscountFactor
discount_factor = interest_rate.discountFactor(start, end)
assert math.isclose(discount_factor, 0.943444995864351)

# Compute equivalent rate
equivalent_rate = interest_rate.equivalentRate(ql.Actual365Fixed(), ql.Simple, ql.Annual, start, end)
assert math.isclose(equivalent_rate.rate(), 0.04)
