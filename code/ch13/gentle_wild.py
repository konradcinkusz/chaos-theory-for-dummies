"""Chapter 13 -- gentle swings and wild ones.

Let go of both arms at the same angle, and of a copy a millionth of a
radian further round, for nine angles from small to nearly upside down.
For each, say when the pair parts, or how close it stayed for twenty
seconds.
"""
# transcript: ch13-gentle-wild

from release import DT, RULE, release
from two_releases import APART, NUDGE, gap

from chaoslab import rk4_step

SECONDS = 20.0


# --8<-- [start:fate]
def fate(angle: float) -> tuple[float | None, float]:
    """When a pair let go at `angle` degrees parts (None if it does not),
    and the largest gap it reached before then."""
    a = release(angle, angle)
    b = (a[0] + NUDGE, a[1], a[2], a[3])
    largest = gap(a, b)
    for step in range(1, round(SECONDS / DT) + 1):
        a, b = rk4_step(RULE, a, DT), rk4_step(RULE, b, DT)
        if gap(a, b) > APART:
            return step * DT, largest
        largest = max(largest, gap(a, b))
    return None, largest
# --8<-- [end:fate]


def main() -> None:
# --8<-- [start:run]
    for angle in range(10, 180, 20):
        seconds, largest = fate(angle)
        if seconds is None:
            print(f"{angle:4d} deg   together; largest gap {largest:.0e} rad")
        else:
            print(f"{angle:4d} deg   apart after {seconds:4.1f} s")
# --8<-- [end:run]


if __name__ == "__main__":
    main()
