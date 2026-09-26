import math

from labs._loader import load


def test_horizon_at_r_four() -> None:
    lab = load("ch07", "l07_02_horizon")
    # at ln 2 per step the error doubles each step: 2**n = 1000
    assert abs(lab.horizon(math.log(2), 1e-6, 1e-3) - math.log2(1000)) < 1e-9
    assert abs(lab.horizon(1.0, 1e-2, 1.0) - math.log(100)) < 1e-12


def test_a_thousand_times_better_is_a_fixed_number_of_steps() -> None:
    lab = load("ch07", "l07_02_horizon")
    lam = math.log(2)
    gain = lab.extra_steps(lam, 1000)
    assert abs(gain - 9.9658) < 1e-3
    # the same gain whatever error you started from
    for delta in (1e-3, 1e-7, 1e-11):
        before = lab.horizon(lam, delta, 0.1)
        after = lab.horizon(lam, delta / 1000, 0.1)
        assert abs((after - before) - gain) < 1e-9


def test_digits_needed() -> None:
    lab = load("ch07", "l07_02_horizon")
    lam = math.log(2)
    assert lab.digits_needed(lam, 100, 0.1) == 32
    assert lab.digits_needed(lam, 1000, 0.1) == 303
    # a system that does not stretch errors needs no more than the tolerance
    assert lab.digits_needed(0.0, 1000, 0.1) == 1
