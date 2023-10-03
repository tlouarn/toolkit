from datetime import date as Date, timedelta

import pandas as pd

from instruments.options import Option
from pricers.black_scholes import BlackScholesParameters, BlackScholesPricer

# This script shows the option decay assuming constant spot
option = Option(strike=4000, maturity=Date(2023, 12, 15), type="CALL")
dates = [Date(2023, 9, 15) + timedelta(days=i) for i in range(92)]

points = []
for date in dates:
    parameters = BlackScholesParameters(spot=4200, interest_rate=0.03, volatility=0.20, pricing_date=date)
    pricer = BlackScholesPricer(option, parameters)
    value = pricer.price()
    points.append({"date": date, "value": value})

points_df = pd.DataFrame(points)
points_df.to_clipboard()
a = 1
