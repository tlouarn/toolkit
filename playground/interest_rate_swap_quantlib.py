# http://gouthamanbalaraman.com/blog/interest-rate-swap-quantlib-python.html

import QuantLib as ql


# Define the calculation date
calculation_date = ql.Date(20, 10, 2015)
ql.Settings.instance().evaluationDate = calculation_date

# Main parameters
risk_free_rate = 0.01
libor_rate = 0.02
day_count = ql.Actual365Fixed()

# Build the discount curve and the libor curve
discount_curve = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
libor_curve = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, libor_rate, day_count))
libor_3m_index = ql.USDLibor(ql.Period(3, ql.Months), libor_curve)

# Compute the fixed leg and floating leg schedules
calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
settle_date = calendar.advance(calculation_date, 5, ql.Days)
maturity_date = calendar.advance(settle_date, 10, ql.Years)

fixed_leg_tenor = ql.Period(6, ql.Months)
fixed_schedule = ql.Schedule(
    settle_date,
    maturity_date,
    fixed_leg_tenor,
    calendar,
    ql.ModifiedFollowing,
    ql.ModifiedFollowing,
    ql.DateGeneration.Forward,
    False,
)

float_leg_tenor = ql.Period(3, ql.Months)
float_schedule = ql.Schedule(
    settle_date,
    maturity_date,
    float_leg_tenor,
    calendar,
    ql.ModifiedFollowing,
    ql.ModifiedFollowing,
    ql.DateGeneration.Forward,
    False,
)

# Create the swap object
notional = 10000000
fixed_rate = 0.025
fixed_leg_daycount = ql.Actual360()
float_spread = 0.004
float_leg_daycount = ql.Actual360()
ir_swap = ql.VanillaSwap(
    ql.VanillaSwap.Payer,
    notional,
    fixed_schedule,
    fixed_rate,
    fixed_leg_daycount,
    float_schedule,
    libor_3m_index,
    float_spread,
    float_leg_daycount,
)

# Attach a pricing engine
swap_engine = ql.DiscountingSwapEngine(discount_curve)
ir_swap.setPricingEngine(swap_engine)

# Get the swap NPV
swap_npv = ir_swap.NPV()
print(swap_npv)
