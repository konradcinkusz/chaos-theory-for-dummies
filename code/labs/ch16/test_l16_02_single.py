import struct

from labs._loader import load


def _single(x: float) -> float:
    return struct.unpack("f", struct.pack("f", x))[0]


def test_rounding_to_single() -> None:
    lab = load("ch16", "l16_02_single")
    assert lab.to_single(0.5) == 0.5
    assert lab.to_single(0.1) == 0.10000000149011612
    assert lab.to_single(1.0 + 1.0 / 2**30) == 1.0


def test_one_single_step() -> None:
    lab = load("ch16", "l16_02_single")
    x = _single(0.1)
    want = _single(_single(4.0 * x) * _single(1.0 - x))
    assert lab.rule_single(x) == want
    assert lab.rule_single(0.5) == 1.0


def test_the_two_precisions_part_where_the_chapter_says() -> None:
    lab = load("ch16", "l16_02_single")
    n = lab.parting_step(0.1, 0.1)
    assert n == 23
    # about as many steps as a single keeps binary digits, and far fewer
    # than a double's 53
    assert 15 <= lab.parting_step(0.3, 0.1) <= 35
    assert lab.parting_step(0.1, 1e-6) < n
