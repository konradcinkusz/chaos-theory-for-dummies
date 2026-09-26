"""Chapter 14 -- weather against climate.

Three long runs of the toy atmosphere: two with the standard forcing
from different starts, and one with the forcing turned up. Each is
boiled down to three statistics -- the kind of number a climate is made
of -- and to the weather at site 0 on its last step, which is the kind
of number a forecast is made of.
"""
# transcript: ch14-climate

import math

from chance_of_rain import RAIN
from ensemble import DT, spin_up

from chaoslab import lorenz96, rk4_step

HOT = 10.0   # the forcing turned up from Lorenz's 8


# --8<-- [start:climate]
def climate(forcing: float, nudge: float,
            steps: int = 10000) -> tuple[float, float, float, float]:
    """Average, typical swing and rain frequency over a long run, and
    the number at site 0 when the run ends."""
    state = spin_up(forcing, nudge)
    field = lorenz96(forcing)
    total = squares = 0.0
    wet = count = 0
    for _ in range(steps):
        state = rk4_step(field, state, DT)
        for x in state:
            total += x
            squares += x * x
            if x > RAIN:
                wet += 1
            count += 1
    average = total / count
    swing = math.sqrt(squares / count - average * average)
    return average, swing, wet / count, state[0]
# --8<-- [end:climate]


def main() -> None:
# --8<-- [start:table]
    print("forcing  nudge   average  swing   rain   last x[0]")
    for forcing, nudge in ((8.0, 0.01), (8.0, 1.0), (HOT, 0.01)):
        average, swing, rain, last = climate(forcing, nudge)
        print(f"{forcing:6.0f}  {nudge:5.2f}  {average:7.1f}  {swing:5.1f}"
              f"  {rain:5.0%}  {last:10.2f}")
# --8<-- [end:table]


if __name__ == "__main__":
    main()
