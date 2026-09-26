import math

from labs._loader import load


def _pair(angle: float, nudge: float) -> tuple[tuple[float, ...], ...]:
    a = (math.radians(angle), math.radians(angle), 0.0, 0.0)
    return a, (a[0] + nudge, a[1], 0.0, 0.0)


def test_the_chapter_pair_parts_after_about_ten_seconds() -> None:
    lab = load("ch13", "l13_02_apart")
    seconds = lab.seconds_until_apart(*_pair(120, 1e-6))
    assert seconds is not None
    assert abs(seconds - 10.21) < 0.05


def test_a_thousand_times_closer_buys_only_seconds() -> None:
    lab = load("ch13", "l13_02_apart")
    millionth = lab.seconds_until_apart(*_pair(120, 1e-6))
    billionth = lab.seconds_until_apart(*_pair(120, 1e-9))
    assert millionth is not None and billionth is not None
    assert 2.0 < billionth - millionth < 6.0


def test_gentle_swings_stay_together() -> None:
    lab = load("ch13", "l13_02_apart")
    assert lab.seconds_until_apart(*_pair(30, 1e-6), limit=20.0) is None


def test_a_bigger_tolerance_takes_longer() -> None:
    lab = load("ch13", "l13_02_apart")
    small = lab.seconds_until_apart(*_pair(120, 1e-6), tol=0.01)
    large = lab.seconds_until_apart(*_pair(120, 1e-6), tol=0.1)
    assert small is not None and large is not None
    assert small < large
