"""Reference solution for Lab 16.2."""

import struct


def to_single(x: float) -> float:
    """The nearest single-precision number to x."""
    return struct.unpack("f", struct.pack("f", x))[0]


def rule_single(x: float) -> float:
    """4x(1 - x), with 4x, 1 - x and their product each rounded to single."""
    return to_single(to_single(4.0 * x) * to_single(1.0 - x))


def parting_step(x0: float, tol: float) -> int:
    """First step at which the double and the single runs differ by > tol."""
    d, s, n = x0, to_single(x0), 0
    while abs(d - s) <= tol:
        d, s, n = 4.0 * d * (1.0 - d), rule_single(s), n + 1
    return n
