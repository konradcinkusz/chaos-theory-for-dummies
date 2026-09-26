from labs._loader import load


def test_settle_skips_then_keeps() -> None:
    lab = load("ch05", "l05_02_period")
    xs = lab.settle(2.8, 0.5, 2, 3)
    assert len(xs) == 3
    # 0.5 -> 0.7 -> 0.588 is skipped over; the kept values start there
    assert abs(xs[0] - 2.8 * 0.7 * 0.3) < 1e-12
    assert abs(xs[1] - 2.8 * xs[0] * (1 - xs[0])) < 1e-12


def test_period_of_made_up_lists() -> None:
    lab = load("ch05", "l05_02_period")
    assert lab.period([0.5] * 10) == 1
    assert lab.period([0.1, 0.2, 0.3] * 20) == 3
    assert lab.period([0.1, 0.2] * 3 + [0.1, 0.25] * 3) is None
    # within the tolerance counts as equal; outside it does not
    assert lab.period([0.4, 0.4 + 1e-12] * 10) == 1
    assert lab.period([0.4, 0.4 + 1e-6] * 10) == 2
    # a cycle longer than you are willing to look for is not found
    assert lab.period([0.1, 0.2, 0.3, 0.4, 0.5] * 10, longest=4) is None


def test_period_of_the_chapters_orbits() -> None:
    lab = load("ch05", "l05_02_period")
    for r, want in ((2.8, 1), (3.2, 2), (3.5, 4), (3.83, 3)):
        assert lab.period(lab.settle(r, 0.2, 2000, 128)) == want, r
    assert lab.period(lab.settle(3.9, 0.2, 2000, 128)) is None
