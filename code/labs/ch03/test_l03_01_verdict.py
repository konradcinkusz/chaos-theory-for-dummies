from labs._loader import load


def crowding(r):
    return lambda x: r * x * (1 - x)


def observed(r: float) -> str:
    """Run the rule from a little above its level and see what happens."""
    f = crowding(r)
    level = 1 - 1 / r
    x = level + 0.001
    sides = []
    for _ in range(2000):
        x = f(x)
        sides.append(x > level)
    if abs(x - level) > 0.001:
        return "pushed away"
    flips = sum(a != b for a, b in zip(sides, sides[1:]))
    return "swings in" if flips > 5 else "creeps in"


def test_fixed_points_are_left_unchanged() -> None:
    lab = load("ch03", "l03_01_verdict")
    for r in (1.5, 2.0, 2.8, 3.1):
        low, high = lab.fixed_points(r)
        assert low == 0.0
        assert abs(high - (1 - 1 / r)) < 1e-12
        assert abs(crowding(r)(high) - high) < 1e-12


def test_the_slopes_the_chapter_measured() -> None:
    lab = load("ch03", "l03_01_verdict")
    for r, s in ((1.5, 0.5), (2.8, -0.8), (3.1, -1.1)):
        assert abs(lab.level_slope(r) - s) < 1e-6


def test_the_verdict_is_what_happens() -> None:
    lab = load("ch03", "l03_01_verdict")
    for r in (1.2, 1.5, 1.8, 2.3, 2.5, 2.8, 2.9, 3.1, 3.2, 3.3):
        assert lab.verdict(r) == observed(r), r
    assert lab.verdict(1.5) == "creeps in"
    assert lab.verdict(2.8) == "swings in"
    assert lab.verdict(3.1) == "pushed away"
