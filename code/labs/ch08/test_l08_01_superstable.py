import math

from labs._loader import load


def test_from_top_takes_the_steps() -> None:
    lab = load("ch08", "l08_01_superstable")
    assert lab.from_top(2.0, 1) == 0.0            # 2 * 0.5 * 0.5 = 0.5
    assert abs(lab.from_top(3.0, 2) - 0.0625) < 1e-15
    assert abs(lab.from_top(3.4, 2) - (0.4335 - 0.5)) < 1e-12


def test_bisect_finds_a_sign_change() -> None:
    lab = load("ch08", "l08_01_superstable")
    root = lab.bisect(lambda x: x * x - 2.0, 1.0, 2.0)
    assert abs(root - math.sqrt(2.0)) < 1e-12
    root = lab.bisect(lambda x: 1.0 - x, 0.0, 3.0)   # falling, not rising
    assert abs(root - 1.0) < 1e-12


def test_the_period_two_landmark_is_one_plus_root_five() -> None:
    lab = load("ch08", "l08_01_superstable")
    assert abs(lab.superstable(2, 3.0, 3.4) - (1 + math.sqrt(5))) < 1e-12


def test_the_heart_of_the_period_three_window() -> None:
    lab = load("ch08", "l08_01_superstable")
    r = lab.superstable(3, 3.82, 3.84)
    assert abs(r - 3.8318740552833) < 1e-9
    assert abs(lab.from_top(r, 3)) < 1e-9
