import struct

from labs._loader import load


def _single(x: float) -> float:
    return struct.unpack("f", struct.pack("f", x))[0]


def _logistic_single(x: float) -> float:
    return _single(_single(4.0 * x) * _single(1.0 - x))


def test_the_generator_of_the_chapter() -> None:
    lab = load("ch16", "l16_03_loops")
    rule = lab.lcg(5, 3, 16)
    xs = [0]
    for _ in range(16):
        xs.append(rule(xs[-1]))
    assert xs[:5] == [0, 3, 2, 13, 4]
    assert sorted(xs[:16]) == list(range(16)) and xs[16] == 0


def test_loops_of_generators() -> None:
    lab = load("ch16", "l16_03_loops")
    assert lab.find_loop(lab.lcg(5, 3, 16), 0) == (0, 16)
    # the doubling map on eight binary digits: dead after eight steps
    assert lab.find_loop(lab.lcg(2, 0, 256), 1) == (8, 1)


def test_the_single_precision_logistic_map_loops() -> None:
    lab = load("ch16", "l16_03_loops")
    assert lab.find_loop(_logistic_single, _single(0.1)) == (1744, 4344)
