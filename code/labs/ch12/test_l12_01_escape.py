from chaoslab import escape_time as library_escape_time
from labs._loader import load


def test_one_step_is_the_multiplication_rule() -> None:
    lab = load("ch12", "l12_01_escape")
    assert lab.step((0.0, 1.0), (0.0, 0.0)) == (-1.0, 0.0)      # i * i
    assert lab.step((3.0, 4.0), (0.0, 0.0)) == (-7.0, 24.0)
    assert lab.step((1.0, 1.0), (0.5, -2.0)) == (0.5, 0.0)


def test_escape_times_from_the_chapter() -> None:
    lab = load("ch12", "l12_01_escape")
    assert lab.escape_time((1.0, 0.0)) == 3        # 0, 1, 2, 5: gone
    assert lab.escape_time((3.0, 0.0)) == 1
    assert lab.escape_time((-1.0, 0.0), limit=50) == 50
    assert lab.escape_time((-2.0, 0.0), limit=50) == 50   # sits on 2
    assert lab.escape_time((0.26, 0.0), limit=1000) == 30
    assert lab.escape_time((0.0, 0.0), limit=10, z=(3.0, 0.0)) == 0


def test_agrees_with_the_library_across_the_plane() -> None:
    lab = load("ch12", "l12_01_escape")
    differ = 0
    for i in range(24):
        for j in range(20):
            a, b = -2.2 + i * 0.12, -1.2 + j * 0.125
            if lab.escape_time((a, b), 60) != library_escape_time(
                    complex(a, b), 60):
                differ += 1
    assert differ <= 5, f"{differ} of 480 points disagree"


def test_the_two_questions() -> None:
    lab = load("ch12", "l12_01_escape")
    assert lab.in_mandelbrot((0.0, 1.0))           # c = i stays
    assert lab.in_mandelbrot((-1.75, 0.0))         # on the needle
    assert not lab.in_mandelbrot((0.26, 0.0))
    assert not lab.in_mandelbrot((-0.8, 0.2))
    # c = 0: the starts that stay are the disc of radius one
    assert lab.in_julia((0.6, 0.7), (0.0, 0.0))
    assert not lab.in_julia((0.6, 0.9), (0.0, 0.0))
    # c = -1: the start 0 is on the cycle 0, -1, 0, -1, ...
    assert lab.in_julia((0.0, 0.0), (-1.0, 0.0))
    assert not lab.in_julia((1.7, 0.0), (-1.0, 0.0))
