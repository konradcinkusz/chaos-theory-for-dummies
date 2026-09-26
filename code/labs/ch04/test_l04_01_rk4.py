import math

from chaoslab import pendulum, rk4_step, spring
from labs._loader import load


def test_one_step_of_growth_matches_the_recipe() -> None:
    # The rule "x grows at a rate equal to x". One step of 1 from 1:
    # k1 = 1, k2 = 1.5, k3 = 1.75, k4 = 2.75, so 1 + (1+3+3.5+2.75)/6.
    lab = load("ch04", "l04_01_rk4")
    (x,) = lab.rk4_step(lambda s: (s[0],), (1.0,), 1.0)
    assert abs(x - (1 + 1 + 1 / 2 + 1 / 6 + 1 / 24)) < 1e-12


def test_agrees_with_chaoslab_on_a_spring_and_a_pendulum() -> None:
    lab = load("ch04", "l04_01_rk4")
    for field, start in ((spring(1.0), (1.0, 0.0)),
                         (pendulum(9.81), (math.radians(60), 0.0))):
        mine = theirs = start
        for _ in range(200):
            mine = lab.rk4_step(field, mine, 0.01)
            theirs = rk4_step(field, theirs, 0.01)
        assert all(abs(a - b) < 1e-12 for a, b in zip(mine, theirs,
                                                      strict=True))


def test_any_number_of_numbers() -> None:
    lab = load("ch04", "l04_01_rk4")

    def still(s: tuple[float, ...]) -> tuple[float, ...]:
        return (0.0, 0.0, 0.0)

    assert tuple(lab.rk4_step(still, (1.0, 2.0, 3.0), 0.5)) == (1.0, 2.0,
                                                                3.0)
