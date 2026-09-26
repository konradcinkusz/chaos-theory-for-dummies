import math

from chaoslab import double_pendulum, double_pendulum_energy, rk4_step
from labs._loader import load


def test_heights_hanging_and_raised() -> None:
    lab = load("ch13", "l13_01_energy")
    h1, h2 = lab.heights((0.0, 0.0, 0.0, 0.0))
    assert abs(h1 + 1.0) < 1e-12 and abs(h2 + 2.0) < 1e-12
    up = math.radians(120)
    h1, h2 = lab.heights((up, up, 0.0, 0.0))
    assert abs(h1 - 0.5) < 1e-12 and abs(h2 - 1.0) < 1e-12


def test_energy_of_the_chapter_release() -> None:
    lab = load("ch13", "l13_01_energy")
    assert abs(lab.energy((0.0, 0.0, 0.0, 0.0)) + 3 * 9.81) < 1e-9
    up = math.radians(120)
    assert abs(lab.energy((up, up, 0.0, 0.0)) - 1.5 * 9.81) < 1e-9


def test_energy_agrees_with_the_library_while_moving() -> None:
    lab = load("ch13", "l13_01_energy")
    for state in [(0.3, -1.1, 2.0, -0.5), (2.5, 1.0, -1.5, 3.0),
                  (-0.7, 2.9, 0.25, 4.0)]:
        assert abs(lab.energy(state) - double_pendulum_energy(state)) < 1e-9


def test_energy_stays_put_along_a_swing() -> None:
    lab = load("ch13", "l13_01_energy")
    rule = double_pendulum()
    state = (math.radians(120), math.radians(120), 0.0, 0.0)
    start = lab.energy(state)
    for _ in range(3000):
        state = rk4_step(rule, state, 0.001)
    assert abs(lab.energy(state) - start) < 1e-6
    assert abs(state[1] - math.radians(120)) > 0.1   # it really moved
