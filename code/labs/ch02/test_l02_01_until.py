import math

from labs._loader import load


def test_counting_steps_for_growth_and_decay() -> None:
    lab = load("ch02", "l02_01_until")
    assert lab.steps_until(1.07, 2.0) == 11      # 7 per cent: the table
    assert lab.steps_until(2.0, 1000.0) == 10    # 2 ** 10 = 1024
    assert lab.steps_until(0.5, 0.01) == 7       # 0.5 ** 7 = 0.0078


def test_the_logarithm_answers_in_fractions_of_a_step() -> None:
    lab = load("ch02", "l02_01_until")
    assert abs(lab.time_until(1.07, 2.0) - 10.2448) < 1e-4
    assert abs(lab.time_until(2.0, 1024.0) - 10.0) < 1e-12
    assert abs(lab.time_until(0.5, 0.01) - 6.6439) < 1e-4


def test_the_count_is_the_logarithm_rounded_up() -> None:
    lab = load("ch02", "l02_01_until")
    for a, ratio in ((1.01, 2.0), (1.05, 3.0), (0.9, 0.5), (0.8, 0.1)):
        assert lab.steps_until(a, ratio) == math.ceil(
            lab.time_until(a, ratio))


def test_half_lives() -> None:
    lab = load("ch02", "l02_01_until")
    assert abs(lab.half_life(0.5) - 1.0) < 1e-12   # the chapter's tablets
    assert abs(lab.half_life(0.2) - 3.1063) < 1e-4
