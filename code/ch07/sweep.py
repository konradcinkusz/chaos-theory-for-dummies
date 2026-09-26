"""Chapter 7 -- the exponent across r: chaos coming and going.

The same average, taken at sixteen settings of the logistic map's knob r,
with chaoslab's lyapunov(), which is the loop of exponent.py with the
settling steps built in.
"""
# transcript: ch07-sweep

from chaoslab import logistic, logistic_slope, lyapunov


def main() -> None:
    # --8<-- [start:sweep]
    print("    r   exponent")
    for k in range(16):
        r = (340 + 4 * k) / 100            # 3.40, 3.44, ..., 4.00
        lam = lyapunov(logistic(r), logistic_slope(r), 0.3, 20_000)
        verdict = "errors grow" if lam > 0 else "errors shrink"
        print(f"{r:5.2f}{lam:+11.2f}   {verdict}")
    # --8<-- [end:sweep]


if __name__ == "__main__":
    main()
