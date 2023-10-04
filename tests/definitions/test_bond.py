from decimal import Decimal

from definitions.date import Date
from instruments.bond import Bond, Frequency, ZeroCouponBond


# def test_construct_gilt():
#     # ISIN GB00BL68HJ26
#
#     gilt = ZeroCouponBond


def test_construct_zero_coupon_bond():
    # OAT = FR0013415627
    oat = ZeroCouponBond(issue=Date(2019, 4, 24), maturity=Date(2025, 3, 25), par=Decimal(100))

    ytm = oat.compute_ytm(Date(2023, 10, 4), Decimal("95.115"))

    a = 1


def test_construct_bond():
    # Gilt GB00BL68HJ26
    gilt = Bond(
        issue=Date(2020, 6, 3),
        maturity=Date(2026, 1, 30),
        par=Decimal(100),
        coupon=Decimal("0.00125"),
        frequency=Frequency.HALF_YEARLY,
    )

    assert isinstance(gilt, Bond)


def test_bond_coupon_dates():
    """
    Test that the coupon dates are correctly computed.
    Example used is the TREASURY GILT 30/01/2026 GB00BL68HJ26.
    """

    gilt = Bond(
        issue=Date(2020, 6, 3),
        maturity=Date(2026, 1, 30),
        par=Decimal(100),
        coupon=Decimal("0.00125"),
        frequency=Frequency.HALF_YEARLY,
    )

    assert gilt.coupon_dates == [
        Date(2021, 1, 30),
        Date(2021, 7, 30),
        Date(2022, 1, 30),
        Date(2022, 7, 30),
        Date(2023, 1, 30),
        Date(2023, 7, 30),
        Date(2024, 1, 30),
        Date(2024, 7, 30),
        Date(2025, 1, 30),
        Date(2025, 7, 30),
        Date(2026, 1, 30),
    ]


def test_bond_yield_to_maturity():
    gilt = Bond(
        issue=Date(2020, 6, 3),
        maturity=Date(2026, 1, 30),
        par=Decimal(100),
        coupon=Decimal("0.00125"),
        frequency=Frequency.HALF_YEARLY,
    )

    trade_date = Date(2023, 10, 4)
    price = Decimal("")
