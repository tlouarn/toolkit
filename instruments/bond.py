import datetime as dt
from dataclasses import dataclass


@dataclass
class Bond:
    coupon: float
    issue_date: dt.date
    maturity: dt.date


class ZeroCouponBond:
    pass


class ConvertibleBond:
    pass


class MandatoryConvertibleBond:
    pass


class PerpetualBond:
    pass
