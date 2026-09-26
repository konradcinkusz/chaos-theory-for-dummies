"""Chapter 12 -- the Mandelbrot set, drawn with characters.

Each character is one value of c. The rule runs from z = 0: a point whose
orbit passes 2 at once is a space, one that lingers gets a denser mark, and
one still inside after LIMIT steps is '@' -- in the set, as far as this many
steps can tell.
"""
# transcript: ch12-ascii

from chaoslab import escape_time

# --8<-- [start:draw]
LIMIT = 50
MARKS = "   ..::--==++**##"     # the later it escapes, the denser the mark


def mark(c: complex) -> str:
    n = escape_time(c, LIMIT)
    return "@" if n == LIMIT else MARKS[min(n, len(MARKS) - 1)]


def main() -> None:
    for row in range(19):                  # top to bottom
        y = (9 - row) / 7.5                # from 1.2 down to -1.2
        line = "".join(mark(complex(-2.1 + col * 0.042, y))
                       for col in range(64))
        print(line.rstrip())
# --8<-- [end:draw]


if __name__ == "__main__":
    main()
