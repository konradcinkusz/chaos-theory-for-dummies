import math

from labs._loader import load


def test_stretch_is_the_slope() -> None:
    lab = load("ch07", "l07_01_exponent")
    assert abs(lab.stretch(4.0, 0.3) - 1.6) < 1e-12
    # the slope is what a tiny nudge is multiplied by: measure it
    r, x, h = 3.7, 0.2, 1e-7

    def f(y: float) -> float:
        return r * y * (1.0 - y)

    nudged = (f(x + h) - f(x - h)) / (2 * h)
    assert abs(lab.stretch(r, x) - nudged) < 1e-6


def test_exponent_at_four_is_ln_two() -> None:
    lab = load("ch07", "l07_01_exponent")
    assert abs(lab.exponent(4.0) - math.log(2)) < 0.01


def test_a_fixed_point_gives_the_log_of_its_slope() -> None:
    lab = load("ch07", "l07_01_exponent")
    # at r = 2.8 the orbit sits on 1 - 1/r, where the slope is 2 - r
    assert abs(lab.exponent(2.8, steps=10_000) - math.log(0.8)) < 1e-9


def test_order_is_negative_and_chaos_is_positive() -> None:
    lab = load("ch07", "l07_01_exponent")
    # a two-cycle: the two slopes multiply to 4 + 2r - r*r
    two = 0.5 * math.log(abs(4 + 2 * 3.2 - 3.2 * 3.2))
    assert abs(lab.exponent(3.2, steps=10_000) - two) < 1e-6
    assert lab.exponent(3.9, steps=20_000) > 0.3
