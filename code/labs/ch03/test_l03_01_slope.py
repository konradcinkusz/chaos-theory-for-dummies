import math

from labs._loader import load


def crowding(r):
    return lambda x: r * x * (1 - x)


def test_slope_of_a_straight_line_is_its_multiplier() -> None:
    lab = load("ch03", "l03_01_slope")
    assert abs(lab.slope(lambda x: 0.9 * x + 2, 5.0) - 0.9) < 1e-6
    assert abs(lab.slope(lambda x: -3 * x, 0.25) + 3) < 1e-6


def test_slope_of_a_curve_depends_on_where_you_are() -> None:
    lab = load("ch03", "l03_01_slope")
    assert abs(lab.slope(lambda x: x * x, 3.0) - 6.0) < 1e-5
    assert abs(lab.slope(lambda x: x * x, -1.0) + 2.0) < 1e-5
    f = crowding(1.5)
    assert abs(lab.slope(f, 1 / 3) - 0.5) < 1e-6
    assert abs(lab.slope(f, 0.0) - 1.5) < 1e-6


def test_fixed_points_are_left_unchanged() -> None:
    lab = load("ch03", "l03_01_slope")
    for r in (1.5, 2.0, 2.8, 3.1):
        low, high = lab.fixed_points(r)
        assert low == 0.0
        assert abs(high - (1 - 1 / r)) < 1e-12
        assert abs(crowding(r)(high) - high) < 1e-12


def test_stability_from_the_slope() -> None:
    lab = load("ch03", "l03_01_slope")
    assert lab.is_stable(crowding(1.5), 1 / 3)
    assert not lab.is_stable(crowding(1.5), 0.0)
    assert lab.is_stable(crowding(2.8), 1 - 1 / 2.8)
    assert not lab.is_stable(crowding(3.1), 1 - 1 / 3.1)
    # Press cos on a calculator over and over: it settles near 0.739.
    assert lab.is_stable(math.cos, 0.7390851332151607)
