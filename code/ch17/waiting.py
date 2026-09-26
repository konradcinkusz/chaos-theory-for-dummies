"""Chapter 17 -- the price of a small nudge is a long wait.

The controller can only act once the orbit is within reach, and the reach
is set by the largest nudge you allow. Start from a thousand different
points, switch the controller on at once, and count the steps until the
first nudge: one run's wait is as unpredictable as the orbit, but the
average over many runs is not.
"""
# transcript: ch17-waiting

from control import R0, nudge, step


# --8<-- [start:wait]
def wait(x: float, largest: float) -> int:
    """Steps from x until the first nudge the controller is allowed."""
    n = 0
    while nudge(x, largest) == 0.0:
        x = step(x, 0.0)
        n += 1
    return n
# --8<-- [end:wait]


def main() -> None:
    # --8<-- [start:table]
    starts = [k / 1001 for k in range(1, 1001)]
    print("largest nudge    average wait    longest wait")
    for percent in (10.0, 1.0, 0.1):
        waits = [wait(x, percent / 100 * R0) for x in starts]
        print(f"{percent:5.1f} per cent   {sum(waits) / len(waits):8.0f}"
              f"      {max(waits):10d}")
    # --8<-- [end:table]


if __name__ == "__main__":
    main()
