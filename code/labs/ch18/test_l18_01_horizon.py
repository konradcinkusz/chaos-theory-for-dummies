import math

from labs._loader import load

LN2 = math.log(2)


def test_six_digits_on_the_logistic_map() -> None:
    lab = load("ch18", "l18_01_horizon")
    # ln(0.1 / 0.000001) / ln 2 = ln(100000) / ln 2
    assert abs(lab.forecast_length(LN2, 6) - 16.61) < 0.01
    assert abs(lab.forecast_length(LN2, 6, tolerance=1.0) - 19.93) < 0.01


def test_every_digit_buys_the_same_steps() -> None:
    lab = load("ch18", "l18_01_horizon")
    gaps = [lab.forecast_length(0.5, d + 1) - lab.forecast_length(0.5, d)
            for d in range(2, 10)]
    assert all(abs(g - math.log(10) / 0.5) < 1e-9 for g in gaps)


def test_a_thousandfold_better_start() -> None:
    lab = load("ch18", "l18_01_horizon")
    assert abs(lab.extra_steps(LN2, 1000) - 9.966) < 0.001
    # twice the exponent, half the gain
    assert abs(lab.extra_steps(2 * LN2, 1000) - 4.983) < 0.001


def test_how_good_the_data_would_have_to_be() -> None:
    lab = load("ch18", "l18_01_horizon")
    # six digits last 16.6 steps: enough for 16, not for 17
    assert lab.digits_needed(LN2, 16) == 6
    assert lab.digits_needed(LN2, 17) == 7
    # a hundred steps of the logistic map need 32 correct digits
    assert lab.digits_needed(LN2, 100) == 32
    assert isinstance(lab.digits_needed(LN2, 10), int)
