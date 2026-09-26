"""Chapter 6 -- two starts one part in ten billion apart, side by side.

Chapter 5's logistic map with its knob turned all the way up, r = 4, run
from 0.2 and from 0.2000000001. Only +, - and * are used, so every digit
printed here is the same on every machine that runs it.
"""
# transcript: ch06-twins

from chaoslab import logistic

# --8<-- [start:twins]
START = 0.2
NUDGE = 1e-10          # one part in ten billion
rule = logistic(4.0)   # x -> 4 * x * (1 - x)


def twin_runs(steps: int) -> tuple[list[float], list[float]]:
    """Run the rule from START and from START + NUDGE; keep every step."""
    a, b = [START], [START + NUDGE]
    for _ in range(steps):
        a.append(rule(a[-1]))
        b.append(rule(b[-1]))
    return a, b
# --8<-- [end:twins]


def main() -> None:
    a, b = twin_runs(40)
    for n in range(0, 41, 5):
        print(f"step {n:2d}:   {a[n]:.10f}   {b[n]:.10f}")


if __name__ == "__main__":
    main()
