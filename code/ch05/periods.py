"""Chapter 5 -- asking a program for the period of an orbit.

Chaoslab's `period` looks at the end of an orbit for the smallest p such
that every value equals the one p steps later. None means that it found no
such p -- which is what a chaotic orbit looks like, and also what a very
long cycle would look like, so None means "not found", never "chaotic".
"""
# transcript: ch05-periods

# --8<-- [start:detect]
from chaoslab import logistic, orbit, period


def main() -> None:
    for r in (2.8, 3.2, 3.5, 3.9, 4.0):
        xs = orbit(logistic(r), 0.2, 2000)     # the start and 2000 steps
        print(f"r = {r}:  period {period(xs)}")
# --8<-- [end:detect]


if __name__ == "__main__":
    main()
