import random

from labs._loader import load

LIBRARY = [0.1, 0.5, 0.9, 0.3]


def _rule(n: int) -> list[float]:
    xs, x = [], 0.3
    for _ in range(n):
        xs.append(x)
        x = 4.0 * x * (1.0 - x)
    return xs


def test_nearest_on_a_library_you_can_read() -> None:
    lab = load("ch15", "l15_02_forecast")
    assert lab.nearest(LIBRARY, 0.52, 1, 1) == [1]
    # 0.3 is the second closest value, but nothing comes after it
    assert lab.nearest(LIBRARY, 0.52, 2, 1) == [1, 2]
    assert lab.nearest(LIBRARY, 0.52, 2, 0) == [1, 3]


def test_forecast_averages_what_came_next() -> None:
    lab = load("ch15", "l15_02_forecast")
    assert lab.forecast(LIBRARY, 0.52, 1) == 0.9
    assert abs(lab.forecast(LIBRARY, 0.52, 1, count=2) - 0.6) < 1e-12
    assert lab.forecast(LIBRARY, 0.12, 2) == 0.9


def test_chaos_is_forecastable_and_noise_is_not() -> None:
    lab = load("ch15", "l15_02_forecast")
    rule = _rule(1000)
    shuf = list(rule)
    random.Random(3).shuffle(shuf)
    assert lab.mean_error(rule, 1, 500) < 0.01
    assert lab.mean_error(shuf, 1, 500) > 0.3
    assert lab.mean_error(rule, 3, 500) > 2 * lab.mean_error(rule, 1, 500)


def test_averaging_several_analogues_helps_with_noise() -> None:
    lab = load("ch15", "l15_02_forecast")
    rng = random.Random(4)
    noisy = [x + rng.uniform(-0.05, 0.05) for x in _rule(1000)]
    one = lab.mean_error(noisy, 1, 500)
    five = lab.mean_error(noisy, 1, 500, count=5)
    assert five < 0.9 * one
