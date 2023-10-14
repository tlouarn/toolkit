from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from definitions.date import Date
from definitions.interest_rate import DayCount, Decimal
from definitions.frequency import Frequency
from definitions.period import Days, Period, Unit


# Useful links and remarks
# https://quant.stackexchange.com/questions/68186/30e-360-bond-payment-schedule


class CouponPayment(str, Enum):
    ANNUAL = "Annual"
    SEMI_ANNUAL = "SemiAnnual"


@dataclass
class Coupon:
    rate: Decimal
    date: Date


class ZeroCouponBond:
    def __init__(self, issue: Date, maturity: Date, par: Decimal):
        self.issue = issue
        self.maturity = maturity
        self.par = par

    def compute_ytm(self, date: Date, price: Decimal) -> Decimal:
        calendar_days = (self.maturity - date).days
        day_count = DayCount.ACTUAL_360
        compounding = Frequency("NoCompounding")
        rate = (self.par / price - 1) * 360 / calendar_days
        return Decimal(rate=rate, day_count=day_count, compounding=compounding)


class Frequency(str, Enum):
    YEARLY = "Yearly"
    HALF_YEARLY = "HalfYearly"

    def to_period(self) -> Period:
        match self:
            case Frequency.ANNUAL:
                return Period(1, Unit.YEAR)
            case Frequency.HALF_YEARLY:
                return Period(6, Unit.MONTH)


class Bond:
    # TODO: COUPON IS AN INTEREST RATE< ACT/365 AND NOCOUMPOUNDING
    def __init__(self, issue: Date, maturity: Date, par: Decimal, face_value: Decimal, coupons: list[Coupon]):
        self.issue = issue
        self.maturity = maturity
        self.par = par
        self.face_value = face_value
        self.coupons = coupons

    def compute_accruals(self, date: Date, price: Decimal) -> Decimal:
        pass

    def compute_ytm(self, date: Date, price: Decimal) -> Decimal:
        pass


# https://www.jdawiseman.com/papers/finmkts/gilt_statics.html

coupon = Decimal(rate=Decimal("0.00125"), compounding=Frequency.YEARLY, day_count=DayCount.ACTUAL_ACTUAL_ISDA)


def gilt(issue: Date, maturity: Date, coupon: Decimal) -> Bond:
    """
    Factory function to create a Bond object based on Gilt characteristics.
    A Gilt is defined by:
       - issue date
       - maturity date
    :param issue: Date
    :param maturity:
    :param coupon: Decimal with the coupon expressed as ACT/365
    :return:
    """


class Gilt(Bond):
    def __init__(self, issue: Date, maturity: Date, coupon: Decimal):
        coupon_dates = []
        super().__init__(issue, maturity, coupon, coupon_dates)

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
        # The first coupon typically occurs at least
        # 60 days after issue date (DMO policy)
        period = self.frequency.to_period()
        while coupon_date > self.issue + Days(60) + period:
            coupon_date = coupon_date - period
            coupon_dates.append(coupon_date)

        return sorted(coupon_dates)
