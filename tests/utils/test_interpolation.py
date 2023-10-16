from decimal import Decimal

import pytest

from utils.interpolate import linear_interpolation


def test_linear_interpolation():
    x1, y1 = Decimal(0), Decimal(10)
    x2, y2 = Decimal(1), Decimal(20)

    # Test interpolation at the boundaries
    assert linear_interpolation(x1, y1, x2, y2, x1) == y1
    assert linear_interpolation(x1, y1, x2, y2, x2) == y2

    # Test interpolation inside the range
    assert linear_interpolation(x1, y1, x2, y2, Decimal("0.1")) == Decimal(11)
    assert linear_interpolation(x1, y1, x2, y2, Decimal("0.5")) == Decimal(15)
    assert linear_interpolation(x1, y1, x2, y2, Decimal("0.9")) == Decimal(19)

    # Test interpolation outside the range
    with pytest.raises(ValueError):
        linear_interpolation(x1, y1, x2, y2, x1 - 1)

    with pytest.raises(ValueError):
        linear_interpolation(x1, y1, x2, y2, x2 + 1)
