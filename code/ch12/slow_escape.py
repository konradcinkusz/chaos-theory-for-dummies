"""Chapter 12 -- how long a point just outside the set takes to leave.

c = 1/4 never escapes. Points a little to its right do, and the closer they
start, the longer the orbit of 0 lingers before it goes.
"""
# transcript: ch12-slow-escape

from chaoslab import escape_time

LIMIT = 10_000


def main() -> None:
    # --8<-- [start:slow]
    for c in (0.3, 0.26, 0.251, 0.2501, 0.25):
        n = escape_time(c, LIMIT)
        if n < LIMIT:
            print(f"c = {c:<6}  passes 2 at step {n}")
        else:
            print(f"c = {c:<6}  still inside after {LIMIT} steps")
    # --8<-- [end:slow]


if __name__ == "__main__":
    main()
