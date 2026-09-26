from chaoslab import cantor, koch
from labs._loader import load


def test_counting_a_few_points() -> None:
    lab = load("ch11", "l11_02_boxes")
    pts = [(0.1, 0.1), (0.2, 0.3), (0.7, 0.7)]
    assert lab.count_boxes(pts, 1.0) == 1
    assert lab.count_boxes(pts, 0.5) == 2
    assert lab.count_boxes(pts, 0.25) == 3


def test_negative_coordinates_use_floor() -> None:
    lab = load("ch11", "l11_02_boxes")
    assert lab.count_boxes([(-0.25, 0.25), (0.25, 0.25)], 1.0) == 2
    assert lab.count_boxes([(0.25, -0.25), (0.25, 0.25)], 1.0) == 2


def test_a_line_and_a_filled_square() -> None:
    lab = load("ch11", "l11_02_boxes")
    sizes = [1 / 2**k for k in range(2, 7)]
    line = [(i / 4096, i / 8192) for i in range(4096)]
    assert abs(lab.box_dimension(line, sizes) - 1) < 0.05
    square = [(i / 256, j / 256) for i in range(256) for j in range(256)]
    assert abs(lab.box_dimension(square, sizes) - 2) < 0.05


def test_the_koch_curve_and_the_cantor_set() -> None:
    lab = load("ch11", "l11_02_boxes")
    koch_sizes = [1 / 2**k for k in range(1, 11)]
    assert abs(lab.box_dimension(koch(8), koch_sizes) - 1.2619) < 0.02
    # The middle of every piece of the Cantor set, laid on the x-axis.
    dust = [((a + b) / 2, 0.0) for a, b in cantor(9)]
    thirds = [1 / 3**k for k in range(1, 7)]
    assert abs(lab.box_dimension(dust, thirds) - 0.6309) < 1e-3
