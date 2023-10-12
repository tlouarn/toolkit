"""
Example taken from
https://www.deriscope.com/excel/blog/InterestRate.xlsx
"""

import QuantLib as ql

interest_rate = ql.InterestRate(0.04, ql.Date(7,9,2018))