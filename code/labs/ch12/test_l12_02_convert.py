import math

from labs._loader import load


def test_r_to_c_at_the_landmarks() -> None:
    lab = load("ch12", "l12_02_convert")
    assert lab.r_to_c(3.0) == -0.75          # where the heart meets a bulb
    assert lab.r_to_c(4.0) == -2.0           # the tip of the needle
    assert lab.r_to_c(1.0) == 0.25           # the cusp of the heart
    assert abs(lab.r_to_c(1 + math.sqrt(8)) - (-1.75)) < 1e-12


def test_c_to_r_undoes_it() -> None:
    lab = load("ch12", "l12_02_convert")
    assert lab.c_to_r(-0.75) == 3.0
    for k in range(31):
        r = 1.0 + k * 0.1
        assert abs(lab.c_to_r(lab.r_to_c(r)) - r) < 1e-9


def test_the_two_rules_walk_in_step() -> None:
    lab = load("ch12", "l12_02_convert")
    for r in (3.2, 3.9):
        c = lab.r_to_c(r)
        x = 0.3
        z = lab.to_z(x, r)
        for _ in range(10):
            x = r * x * (1 - x)
            z = z * z + c
            assert abs(z - lab.to_z(x, r)) < 1e-9


def test_the_doublings_land_on_the_bulbs() -> None:
    lab = load("ch12", "l12_02_convert")
    cs = lab.doublings_in_c()
    assert len(cs) == 5
    assert cs[0] == -0.75
    assert abs(cs[1] - (-1.25)) < 1e-12
    assert all(a > b for a, b in zip(cs, cs[1:], strict=False))
    assert abs(cs[-1] - (-1.401155)) < 1e-5     # the Feigenbaum point
