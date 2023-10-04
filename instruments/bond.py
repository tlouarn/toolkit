from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from definitions.date import Date
from definitions.interest_rate import Compounding, DayCount, InterestRate
from definitions.period import Period, Unit


@dataclass
class Coupon:
    rate: InterestRate
    date: Date


class ZeroCouponBond:
    def __init__(self, issue: Date, maturity: Date, par: Decimal):
        self.issue = issue
        self.maturity = maturity
        self.par = par

    def compute_ytm(self, date: Date, price: Decimal) -> InterestRate:
        calendar_days = (self.maturity - date).days
        day_count = DayCount.ACT_360
        compounding = Compounding("NoCompounding")
        rate = (self.par / price - 1) * 360 / calendar_days
        return InterestRate(rate=rate, day_count=day_count, compounding=compounding)


class Frequency(str, Enum):
    YEARLY = "Yearly"
    HALF_YEARLY = "HalfYearly"

    def to_period(self) -> Period:
        match self:
            case Frequency.YEARLY:
                return Period(1, Unit.YEAR)
            case Frequency.HALF_YEARLY:
                return Period(6, Unit.MONTH)


class Bond:
    # TODO: COUPON IS AN INTEREST RATE< ACT/365 AND NOCOUMPOUNDING
    def __init__(self, issue: Date, maturity: Date, par: Decimal, coupon: Decimal, frequency: Frequency):
        self.issue = issue
        self.maturity = maturity
        self.par = par
        self.coupon = coupon
        self.frequency = frequency

    @property
    def coupon_dates(self) -> list[Date]:
        """
        Coupon dates are typically unadjusted for weekends or holidays.
        :return: a list of Date objects corresponding to the coupon payment dates.
        """
        coupon_dates = []

        # A bond with a coupon of 0 does not pay coupons
        if self.coupon == Decimal(0):
            return coupon_dates

        # The last coupon is paid on maturity date
        coupon_date = self.maturity
        coupon_dates.append(coupon_date)

        # Go backwards and add the periodic coupons
        # The first coupon typically does not happen if
        # less than a period away from the issue date
        period = self.frequency.to_period()
        while coupon_date > self.issue + period * 2:
            coupon_date = coupon_date - period
            coupon_dates.append(coupon_date)

        return sorted(coupon_dates)

    def compute_accruals(self, date: Date, price: Decimal) -> Decimal:
        pass

    def compute_ytm(self, date: Date, price: Decimal) -> InterestRate:
        pass



# https://www.jdawiseman.com/papers/finmkts/gilt_statics.html


class ConventionalGilt(Bond):

    def __init__(self, issue: Date, maturity: Date, coupon: Decimal):
        coupon_dates = []
        super().__init__(issue, maturity, coupon, coupon_dates)



