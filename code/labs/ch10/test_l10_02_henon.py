from labs._loader import load


def test_the_first_steps_from_the_origin() -> None:
    lab = load("ch10", "l10_02_henon")
    assert lab.step(0.0, 0.0) == (1.0, 0.0)
    x, y = lab.step(1.0, 0.0)
    assert abs(x + 0.4) < 1e-12 and abs(y - 0.3) < 1e-12
    x, y = lab.step(0.5, 0.0)
    assert abs(x - 0.65) < 1e-12 and abs(y - 0.15) < 1e-12


def test_other_numbers_give_another_rule() -> None:
    lab = load("ch10", "l10_02_henon")
    x, y = lab.step(1.0, 2.0, a=1.0, b=0.5)
    assert abs(x - 2.0) < 1e-12 and abs(y - 0.5) < 1e-12


def test_area_shrinks_by_b_everywhere() -> None:
    lab = load("ch10", "l10_02_henon")
    for x, y in [(0.0, 0.0), (0.7, -0.2), (-1.1, 0.3), (1.25, 0.05)]:
        assert abs(lab.area_factor(x, y) - 0.3) < 1e-5
    assert abs(lab.area_factor(0.4, 0.1, b=0.5) - 0.5) < 1e-5
    assert abs(lab.area_factor(0.4, 0.1, a=2.0, b=0.1) - 0.1) < 1e-5
