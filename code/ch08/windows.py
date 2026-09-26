"""Chapter 8 -- a window of order inside the chaos.

Past r = 3.5699 the doublings are used up, and most values of r give an
orbit that never repeats. Not all of them. Walk r across one stretch and
ask, at each stop, what the orbit has settled into.
"""
# transcript: ch08-windows

import math

from doublings import settled_period
from superstable import landmarks, ratios

from chaoslab import logistic


def main() -> None:
    print("     r   period")
    for r in (3.82, 3.8284, 3.8285, 3.83, 3.84, 3.845, 3.848, 3.85, 3.86):
        p = settled_period(r)
        print(f"{r:6}   {p if p else '-':>6}")
    print(f"the window opens at 1 + sqrt(8) = {1 + math.sqrt(8):.5f}")
    found = landmarks(logistic, (3.82, 3.84), (3.84, 3.848), 9, base=3)
    print(f"periods 3, 6, 12, ...: last ratio {ratios(found)[-1]:.3f}")


if __name__ == "__main__":
    main()
