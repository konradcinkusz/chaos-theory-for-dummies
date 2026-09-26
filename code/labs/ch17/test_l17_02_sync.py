import math

from labs._loader import load


def test_the_copy_obeys_the_same_rules_with_the_given_x() -> None:
    lab = load("ch17", "l17_02_sync")
    s = (1.0, 2.0, 3.0, 4.0, 5.0)
    got = lab.copy_field(s)
    beta = 8.0 / 3.0
    want = (10.0 * (2.0 - 1.0),
            1.0 * (28.0 - 3.0) - 2.0,
            1.0 * 2.0 - beta * 3.0,
            1.0 * (28.0 - 5.0) - 4.0,
            1.0 * 4.0 - beta * 5.0)
    assert len(got) == 5
    assert all(abs(a - b) < 1e-12 for a, b in zip(got, want, strict=True))


def test_error_measures_only_the_copy() -> None:
    lab = load("ch17", "l17_02_sync")
    assert lab.error((7.0, 1.0, 2.0, 4.0, 6.0)) == 5.0
    assert lab.error((7.0, 1.0, 2.0, 1.0, 2.0)) == 0.0


def test_the_copy_falls_into_step() -> None:
    lab = load("ch17", "l17_02_sync")
    t6 = lab.sync_time(1e-6)
    t9 = lab.sync_time(1e-9)
    assert 8.0 < t6 < 12.0
    # the error is guaranteed to fall at least by a factor e per time unit,
    # so three more factors of ten can take no longer than 3 * ln(10)
    assert 0.0 < t9 - t6 < 3.0 * math.log(10.0)
