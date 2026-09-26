import math

from chaoslab import logistic
from labs._loader import load


def tea(temp: float) -> float:
    return temp - 0.1 * (temp - 20.0)


def test_the_tea_forgets_and_the_logistic_map_does_not() -> None:
    lab = load("ch18", "l18_02_guide")
    assert lab.error_grows(tea, 90.0) is False
    assert lab.error_grows(logistic(2.8), 0.3) is False
    assert lab.error_grows(logistic(4.0), 0.3) is True


def test_growth_rates() -> None:
    lab = load("ch18", "l18_02_guide")
    # the tea's gap is multiplied by 0.9 every minute, exactly
    rate = lab.growth_rate(tea, 90.0, delta=1e-6)
    assert abs(rate - math.log(0.9)) < 1e-4
    # the logistic map's is about ln 2, averaged over a few starts
    starts = (0.2, 0.3, 0.4, 0.6, 0.7)
    mean = sum(lab.growth_rate(logistic(4.0), x) for x in starts) / 5
    assert 0.5 < mean < 0.9


def test_the_long_run_is_predictable_when_the_path_is_not() -> None:
    lab = load("ch18", "l18_02_guide")
    rule = logistic(4.0)
    a = lab.long_run_fraction(rule, 0.3, 0.0, 0.25)
    b = lab.long_run_fraction(rule, 0.8, 0.0, 0.25)
    assert abs(a - 1 / 3) < 0.01 and abs(b - 1 / 3) < 0.01
    assert lab.long_run_fraction(tea, 90.0, 20.0, 21.0, 1000) > 0.9
