from chaoslab import euler_step, rk4_step
from labs._loader import load


def test_energy_of_a_spring() -> None:
    lab = load("ch04", "l04_02_drift")
    assert lab.spring_energy((1.0, 0.0)) == 0.5
    assert abs(lab.spring_energy((0.6, 0.8)) - 0.5) < 1e-15
    assert lab.spring_energy((0.0, 2.0)) == 2.0


def test_euler_gains_exactly_one_per_cent_a_step() -> None:
    # Each Euler step of 0.1 multiplies the energy by 1 + 0.1 * 0.1.
    lab = load("ch04", "l04_02_drift")
    assert abs(lab.drift(euler_step, 0.1, 10) - (1.01 ** 100 - 1)) < 1e-9


def test_a_smaller_step_is_right_for_longer_not_right() -> None:
    lab = load("ch04", "l04_02_drift")
    coarse = lab.drift(euler_step, 0.1, 10)
    fine = lab.drift(euler_step, 0.01, 10)
    fine_long = lab.drift(euler_step, 0.01, 100)
    assert fine < coarse / 10          # much better over the same time
    assert abs(fine_long / coarse - 1) < 0.02   # same gain, ten times later


def test_rk4_holds_the_energy() -> None:
    lab = load("ch04", "l04_02_drift")
    d = lab.drift(rk4_step, 0.1, 10)
    assert -1e-5 < d < 0.0             # a very slight loss


def test_halving_the_step() -> None:
    # Euler's drift only about halves; RK4's shrinks about thirty-two-fold.
    lab = load("ch04", "l04_02_drift")
    assert 1.9 < lab.halving(euler_step, 0.01, 10) < 2.2
    assert 30 < lab.halving(rk4_step, 0.1, 10) < 34
