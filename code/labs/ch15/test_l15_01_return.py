import random

from labs._loader import load


def _rule(n: int) -> list[float]:
    xs, x = [], 0.3
    for _ in range(n):
        xs.append(x)
        x = 4.0 * x * (1.0 - x)
    return xs


def test_pairs_are_each_value_and_the_next() -> None:
    lab = load("ch15", "l15_01_return")
    assert lab.return_pairs([0.1, 0.2, 0.3]) == [(0.1, 0.2), (0.2, 0.3)]
    assert lab.return_pairs([0.5]) == []


def test_squares_on_a_series_you_can_count_by_hand() -> None:
    lab = load("ch15", "l15_01_return")
    assert lab.squares_touched([0.05, 0.95, 0.05, 0.95]) == 2
    # a value of exactly 1 belongs in the last square, not off the edge
    assert lab.squares_touched([0.0, 1.0, 0.5], k=2) == 2
    assert lab.squares_touched([0.25, -0.01, 0.75], k=2) == 2


def test_the_rule_draws_a_curve_and_the_shuffle_a_cloud() -> None:
    lab = load("ch15", "l15_01_return")
    rule = _rule(2000)
    shuf = list(rule)
    random.Random(1).shuffle(shuf)
    assert lab.squares_touched(rule) <= 30
    assert lab.squares_touched(shuf) >= 95
    assert lab.verdict(rule) == "curve"
    assert lab.verdict(shuf) == "cloud"


def test_a_cycle_is_a_curve_too() -> None:
    lab = load("ch15", "l15_01_return")
    assert lab.verdict([0.2, 0.5, 0.8] * 100) == "curve"
    assert lab.verdict([0.2, 0.5, 0.8] * 100, k=2) == "cloud"
