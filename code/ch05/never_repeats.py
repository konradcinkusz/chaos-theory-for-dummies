"""Chapter 5 -- a hundred thousand steps, and no value comes back.

If any value came back exactly, every value after it would come back too,
because the same number always gives the same next number. So counting how
many DIFFERENT values an orbit has visited is a test for a cycle -- and
running the same start twice is a test of the rule itself.
"""
# transcript: ch05-never-repeats

# --8<-- [start:count]
from chaoslab import logistic, orbit


def main() -> None:
    for r in (3.9, 4.0):
        xs = orbit(logistic(r), 0.2, 100_000)
        again = orbit(logistic(r), 0.2, 100_000)
        print(f"r = {r}: {len(xs)} values, {len(set(xs))} different")
        print(f"         same start again, same list: {xs == again}")
# --8<-- [end:count]


if __name__ == "__main__":
    main()
