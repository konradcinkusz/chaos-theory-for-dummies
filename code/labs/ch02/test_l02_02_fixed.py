import pytest

from labs._loader import load


def test_fixed_points_of_the_chapter_rules() -> None:
    lab = load("ch02", "l02_02_fixed")
    assert lab.fixed_point(0.5, 100.0) == 200.0          # the tablets
    assert abs(lab.fixed_point(0.9, 2.0) - 20.0) < 1e-9  # the tea
    assert abs(lab.fixed_point(1.01, -100.0) - 10000.0) < 1e-6  # the loan
    assert abs(lab.fixed_point(-0.5, 57.0) - 38.0) < 1e-12      # the shower


def test_a_rule_that_only_adds_has_no_fixed_point() -> None:
    lab = load("ch02", "l02_02_fixed")
    with pytest.raises(ValueError):
        lab.fixed_point(1.0, 50.0)


def test_stability_depends_on_the_size_of_a() -> None:
    lab = load("ch02", "l02_02_fixed")
    assert lab.is_stable(0.5, 100.0)
    assert lab.is_stable(-0.5, 57.0)
    assert not lab.is_stable(1.01, -100.0)
    assert not lab.is_stable(-1.5, 95.0)
    assert not lab.is_stable(2.0, 0.0)


def test_steps_to_settle() -> None:
    lab = load("ch02", "l02_02_fixed")
    assert lab.steps_to_settle(0.5, 100.0, 100.0, 1.0) == 7
    assert lab.steps_to_settle(-0.5, 57.0, 30.0, 0.1) == 7
    with pytest.raises(ValueError):
        lab.steps_to_settle(1.01, -100.0, 11000.0, 1.0)
