from labs._loader import load


def test_the_fixed_point_is_left_unchanged() -> None:
    lab = load("ch05", "l05_01_stability")
    assert abs(lab.fixed_point(2.0) - 0.5) < 1e-12
    assert abs(lab.fixed_point(4.0) - 0.75) < 1e-12
    for r in (1.5, 2.8, 3.2, 3.9):
        x = lab.fixed_point(r)
        assert abs(r * x * (1 - x) - x) < 1e-12


def test_the_slope_is_measured_not_guessed() -> None:
    lab = load("ch05", "l05_01_stability")
    # at the top of the hump a nudge is flattened: the slope is zero
    assert abs(lab.slope_at(3.9, 0.5)) < 1e-6
    # at the fixed point the measured slope is 2 - r, as the chapter found
    for r in (2.8, 3.2, 3.5):
        assert abs(lab.slope_at(r, lab.fixed_point(r)) - (2 - r)) < 1e-5
    # and it is a measurement at the point you give it, not a formula for r
    assert abs(lab.slope_at(3.0, 0.25) - 1.5) < 1e-5


def test_holds_below_three_and_not_above() -> None:
    lab = load("ch05", "l05_01_stability")
    assert lab.holds(2.8) is True
    assert lab.holds(2.99) is True
    assert lab.holds(3.01) is False
    assert lab.holds(3.2) is False


def test_it_lets_go_at_three() -> None:
    lab = load("ch05", "l05_01_stability")
    assert abs(lab.lets_go(2.5, 3.5) - 3.0) < 1e-6
    assert abs(lab.lets_go(2.9, 3.3, tol=1e-12) - 3.0) < 1e-6
