from definitions.discount_curve import DiscountCurve
from definitions.interest_rate import Decimal
from instruments.interest_rate_swap import FixedLeg, FloatingLeg, InterestRateSwap


def value_fixed_leg(fixed_leg: FixedLeg, discount_curve: DiscountCurve) -> Decimal:
    npv = Decimal(0)

    for coupon in fixed_leg.coupons:
        discount_factor = discount_curve.get(coupon.payment)
        npv += coupon.amount * discount_factor

    return npv


def value_floating_leg(floating_leg: FloatingLeg, ibor_curve: DiscountCurve, discount_curve: DiscountCurve) -> Decimal:
    # Imply the forward Ibor rates from ibor_curve

    for coupon in floating_leg.coupons:
        forward_rate = ibor_curve.forward(coupon.start, coupon.end)
        days = coupon.end - coupon.start
        amount = floating_leg.notional * forward_rate * days

def value_irs(swap: InterestRateSwap, ibor_curve: DiscountCurve, discount_curve: DiscountCurve) -> Decimal:
    # Value the fixed leg
    fixed_
