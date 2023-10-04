from definitions.interest_rate import Compounding, DayCount, InterestRate


def test_instantiate_interest_rate():
    rate = 0.03
    compounding = Compounding.NO_COMPOUNDING
    day_count = DayCount.ACT_360
    interest_rate = InterestRate(rate, compounding, day_count)

    assert interest_rate.rate == rate
    assert interest_rate.compounding == compounding
    assert interest_rate.day_count == day_count


def test_effective_rate():
    rate = 0.06
    compounding = Compounding.MONTHLY
    day_count = DayCount.ACT_360
    interest_rate = InterestRate(rate=rate, compounding=compounding, day_count=day_count)

    assert round(interest_rate.effective, 4) == 0.0617

    a = 1
