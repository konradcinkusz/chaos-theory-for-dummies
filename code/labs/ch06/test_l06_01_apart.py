from chaoslab import logistic, steps_until_apart
from labs._loader import load


def doubler(x: float) -> float:
    return 2 * x


def tea(temp: float) -> float:
    return temp - 0.1 * (temp - 20.0)


def test_gaps_keeps_every_step() -> None:
    lab = load("ch06", "l06_01_apart")
    assert lab.gaps(doubler, 0.0, 0.001, 3) == [0.001, 0.002, 0.004, 0.008]


def test_a_gap_that_doubles_passes_one_after_ten_steps() -> None:
    lab = load("ch06", "l06_01_apart")
    # 0.001 doubled nine times is 0.512; ten times is 1.024
    assert lab.first_apart(doubler, 0.0, 0.001, 1.0) == 10
    assert lab.first_apart(doubler, 0.2, 0.9, 0.5) == 0


def test_the_twins_of_the_chapter() -> None:
    lab = load("ch06", "l06_01_apart")
    rule = logistic(4.0)
    n = lab.first_apart(rule, 0.2, 0.2 + 1e-10, 0.1)
    assert n == 30
    assert n == steps_until_apart(rule, 0.2, 1e-10, 0.1)


def test_the_tea_never_parts_company() -> None:
    lab = load("ch06", "l06_01_apart")
    assert lab.first_apart(tea, 90.0, 91.0, 2.0) is None
    assert lab.gaps(tea, 90.0, 91.0, 30)[-1] < 0.05
