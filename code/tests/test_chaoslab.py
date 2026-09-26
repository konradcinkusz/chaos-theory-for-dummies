"""chaoslab, watched producing answers that are known in advance.

Each test pins a function to a number that is established independently of
it -- a fixed point from algebra, a Lyapunov exponent that is exactly ln 2,
an energy that must not move -- so a green run means the library measures
the thing the book says it measures, not merely that it runs.
"""

from __future__ import annotations

import math

import chaoslab as cl


def test_orbit_keeps_the_start_and_every_step() -> None:
    xs = cl.orbit(cl.linear(2.0, 0.0), 1.0, 5)
    assert xs == [1.0, 2.0, 4.0, 8.0, 16.0, 32.0]


def test_logistic_settles_on_its_fixed_point() -> None:
    r = 2.8
    xs = cl.orbit(cl.logistic(r), 0.2, 500)
    assert abs(xs[-1] - (1 - 1 / r)) < 1e-12
    assert cl.period(xs) == 1


def test_period_two_and_none() -> None:
    assert cl.period(cl.orbit(cl.logistic(3.2), 0.2, 2000)) == 2
    assert cl.period(cl.orbit(cl.logistic(3.5), 0.2, 2000)) == 4
    assert cl.period(cl.orbit(cl.logistic(4.0), 0.2, 2000)) is None


def test_slope_matches_the_formula() -> None:
    r = 3.0
    assert abs(cl.slope(cl.logistic(r), 0.3) - r * (1 - 0.6)) < 1e-8


def test_rk4_holds_energy_and_euler_does_not() -> None:
    field = cl.spring()
    start = (1.0, 0.0)
    rk = cl.integrate(field, start, 0.01, 1000)
    eu = cl.integrate(field, start, 0.01, 1000, stepper=cl.euler_step)

    def energy(s: tuple[float, ...]) -> float:
        return 0.5 * (s[0] ** 2 + s[1] ** 2)

    assert abs(energy(rk[-1]) - 0.5) < 1e-9
    assert energy(eu[-1]) > 0.5 * 1.1


def test_logistic_at_four_has_exponent_ln2() -> None:
    lam = cl.lyapunov(cl.logistic(4.0), cl.logistic_slope(4.0), 0.3, 200_000)
    assert abs(lam - math.log(2)) < 0.01


def test_periodic_window_has_negative_exponent() -> None:
    lam = cl.lyapunov(cl.logistic(3.2), cl.logistic_slope(3.2), 0.3, 20_000)
    assert lam < 0


def test_lorenz_exponent_is_about_point_nine() -> None:
    lam = cl.lyapunov_flow(cl.lorenz(), (1.0, 1.0, 1.0), 0.01, 20_000)
    assert 0.8 < lam < 1.0


def test_separation_starts_at_delta_and_grows() -> None:
    gaps = cl.separation(cl.logistic(4.0), 0.3, 1e-10, 40)
    # 0.3 + 1e-10 is rounded when it is stored, so the first gap is
    # 1e-10 to about seven figures, not exactly: Chapter 16 is about that.
    assert abs(gaps[0] - 1e-10) < 1e-16
    assert max(gaps) > 0.1


def test_horizon_is_logarithmic() -> None:
    assert abs(cl.horizon(math.log(2), 1e-6, 1e-3) - math.log2(1000)) < 1e-9


def test_henon_contracts_area_by_b() -> None:
    f = cl.henon()
    # the Jacobian of (1 - a x^2 + y, b x) has determinant -b everywhere
    h, p = 1e-6, (0.3, 0.2)
    fx = f((p[0] + h, p[1]))
    fy = f((p[0], p[1] + h))
    f0 = f(p)
    det = ((fx[0] - f0[0]) * (fy[1] - f0[1])
           - (fy[0] - f0[0]) * (fx[1] - f0[1])) / (h * h)
    assert abs(abs(det) - 0.3) < 1e-4


def test_koch_and_cantor_counts() -> None:
    assert len(cl.koch(1)) == 5
    assert len(cl.koch(3)) == 4 ** 3 + 1
    assert len(cl.cantor(4)) == 16


def test_escape_time() -> None:
    assert cl.escape_time(0j) == 100
    assert cl.escape_time(1 + 1j) < 5
    assert cl.r_to_c(4.0) == -2.0


def test_doubling_map_collapses_to_zero_on_floats() -> None:
    xs = cl.orbit(cl.doubling, 0.1, 80)
    assert xs[-1] == 0.0


def test_box_count_and_fit() -> None:
    line = [(i / 1000, 0.0) for i in range(1000)]
    assert cl.box_count(line, 0.1) == 10
    assert abs(cl.fit_slope([0.0, 1.0, 2.0], [1.0, 3.0, 5.0]) - 2.0) < 1e-12
