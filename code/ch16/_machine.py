"""Chapter 16 helpers -- single precision, and finding a machine's loops.

Imported by the chapter's measurements and plots rather than run. Python's
float is double precision; single precision is emulated by packing a
number into the four bytes of a single and reading it back, which rounds it
to the nearest single exactly as single-precision hardware would.
"""

import struct
from collections.abc import Callable


def to_single(x: float) -> float:
    """The nearest single-precision number to x."""
    return struct.unpack("f", struct.pack("f", x))[0]


def rule_single(x: float) -> float:
    """4x(1 - x) with every operation rounded to single precision."""
    return to_single(to_single(4.0 * x) * to_single(1.0 - x))


def find_loop(rule: Callable[[float], float], x0: float) -> tuple[int, int]:
    """(steps before the loop, length of the loop) for the orbit of x0.

    A computer holds finitely many numbers, so every orbit on it repeats.
    Remember the step at which each value was first seen; the first value
    seen twice closes the loop.
    """
    seen: dict[float, int] = {}
    x, n = x0, 0
    while x not in seen:
        seen[x] = n
        x, n = rule(x), n + 1
    return seen[x], n - seen[x]


def bits_kept(rounder: Callable[[float], float]) -> int:
    """How many significant binary digits a format keeps, measured: the
    smallest k for which 1 + 1/2**k is rounded back to exactly 1."""
    k = 1
    while rounder(1.0 + 1.0 / 2**k) != 1.0:
        k += 1
    return k
