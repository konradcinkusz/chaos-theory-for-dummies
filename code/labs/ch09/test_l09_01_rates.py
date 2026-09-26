import math

from chaoslab import lorenz
from labs._loader import load


def test_rates_at_two_states() -> None:
    lab = load("ch09", "l09_01_rates")
    dx, dy, dz = lab.rates((1.0, 1.0, 1.0))
    assert dx == 0.0 and dy == 26.0
    assert abs(dz - (1.0 - 8.0 / 3.0)) < 1e-12
    dx, dy, dz = lab.rates((2.0, 3.0, 4.0))
    assert (dx, dy) == (10.0, 45.0)
    assert abs(dz - (6.0 - 32.0 / 3.0)) < 1e-12


def test_rates_agree_with_chaoslab_at_other_settings() -> None:
    lab = load("ch09", "l09_01_rates")
    for sigma, rho, beta in [(10.0, 28.0, 8.0 / 3.0), (16.0, 45.0, 4.0)]:
        field = lorenz(sigma, rho, beta)
        for s in [(1.0, -2.0, 3.0), (-7.5, 4.25, 30.0)]:
            mine = lab.rates(s, sigma, rho, beta)
            theirs = field(s)
            assert all(abs(p - q) < 1e-12
                       for p, q in zip(mine, theirs, strict=True))


def test_three_fixed_points_when_heated() -> None:
    lab = load("ch09", "l09_01_rates")
    points = lab.fixed_points(28.0)
    assert len(points) == 3
    assert points[0] == (0.0, 0.0, 0.0)
    assert abs(points[1][0] - math.sqrt(72.0)) < 1e-12
    assert abs(points[2][1] + math.sqrt(72.0)) < 1e-12
    for p in points:
        assert all(abs(r) < 1e-9 for r in lab.rates(p))
    for p in lab.fixed_points(20.0, 3.0):
        assert all(abs(r) < 1e-9 for r in lab.rates(p, rho=20.0, beta=3.0))


def test_one_fixed_point_when_barely_heated() -> None:
    lab = load("ch09", "l09_01_rates")
    assert lab.fixed_points(0.5) == [(0.0, 0.0, 0.0)]
