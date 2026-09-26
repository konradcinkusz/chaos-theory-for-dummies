"""Chapter 13 -- two double pendulums let go a millionth of a radian apart.

The same rule, the same step, the same release, except that the upper arm
of the second pendulum starts one millionth of a radian further round:
about a thousandth of a millimetre at the end of a one-metre arm. The gap
between the two is printed every second until it passes a tenth of a
radian, about six degrees, which anybody could see.
"""
# transcript: ch13-two-releases

from release import DT, RULE, release

from chaoslab import rk4_step

NUDGE = 1e-6    # radians: the difference between the two releases
APART = 0.1     # radians: about six degrees, a gap anyone can see


# --8<-- [start:gap]
def gap(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    """How far apart two pendulums are: the larger of the two angle gaps."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
# --8<-- [end:gap]


def main() -> None:
# --8<-- [start:run]
    a = release(120, 120)
    b = (a[0] + NUDGE, a[1], a[2], a[3])
    step = 0
    while gap(a, b) <= APART:
        if step % 1000 == 0:
            print(f"t = {step * DT:4.1f} s   gap {gap(a, b):.0e} rad")
        a, b = rk4_step(RULE, a, DT), rk4_step(RULE, b, DT)
        step += 1
    print(f"more than {APART} rad apart after {step * DT:.1f} s")
# --8<-- [end:run]


if __name__ == "__main__":
    main()
