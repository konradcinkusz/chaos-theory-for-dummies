"""Chapter 14 -- an ensemble forecast on Lorenz's toy atmosphere.

We play nature with one run of the model, the truth; measure it with a
small error, the analysis; and forecast from twenty copies of the
analysis, each nudged by an error of the same size. The rule is
chaoslab.lorenz96, which uses only + - * /, and the errors come from
random.uniform, which is arithmetic too, so every digit printed here is
the same on every machine.
"""
# transcript: ch14-ensemble

import math
import random

from chaoslab import lorenz96, rk4_step

State = tuple[float, ...]

# --8<-- [start:setup]
N = 40           # numbers round the circle of latitude
FORCING = 8.0    # the drive: Lorenz's standard value
DT = 0.05        # one step; about six hours in Lorenz's units
ERROR = 0.1      # the analysis is right to within 0.1 on every number
MEMBERS = 20     # copies in the ensemble


def run(state: State, steps: int, forcing: float = FORCING) -> State:
    """Follow the toy atmosphere for a number of steps."""
    field = lorenz96(forcing)
    for _ in range(steps):
        state = rk4_step(field, state, DT)
    return state


def spin_up(forcing: float = FORCING, nudge: float = 0.01) -> State:
    """A calm atmosphere with one number nudged, left to make weather."""
    calm = (forcing + nudge,) + (forcing,) * (N - 1)
    return run(calm, 2000, forcing)


def perturb(state: State, size: float, rng: random.Random) -> State:
    """Add an error no bigger than `size` to every number."""
    return tuple(x + rng.uniform(-size, size) for x in state)
# --8<-- [end:setup]


# --8<-- [start:scores]
def mean(members: list[State]) -> State:
    """The ensemble mean: each number averaged over the members."""
    return tuple(sum(xs) / len(xs) for xs in zip(*members, strict=True))


def spread(members: list[State]) -> float:
    """How far the members typically sit from their own mean."""
    centre = mean(members)
    total = 0.0
    for state in members:
        for x, c in zip(state, centre, strict=True):
            total += (x - c) * (x - c)
    return math.sqrt(total / (len(members) * N))


def error(state: State, truth: State) -> float:
    """How far a forecast typically sits from the truth."""
    total = 0.0
    for x, t in zip(state, truth, strict=True):
        total += (x - t) * (x - t)
    return math.sqrt(total / N)
# --8<-- [end:scores]


# --8<-- [start:forecast]
def ensemble(truth: State, rng: random.Random) -> tuple[State, list[State]]:
    """An analysis of `truth`, and MEMBERS copies of it, each nudged."""
    analysis = perturb(truth, ERROR, rng)
    return analysis, [perturb(analysis, ERROR, rng) for _ in range(MEMBERS)]


def forecast(truth: State, rng: random.Random,
             leads: range) -> list[tuple[float, float, float, float]]:
    """Score an ensemble forecast at each lead (counted in steps): the
    spread, the error of the ensemble mean, and the error of one run
    from the analysis alone."""
    single, members = ensemble(truth, rng)
    done, rows = 0, []
    for lead in leads:
        gap = lead - done
        truth = run(truth, gap)
        single = run(single, gap)
        members = [run(m, gap) for m in members]
        done = lead
        rows.append((lead * DT, spread(members),
                     error(mean(members), truth), error(single, truth)))
    return rows
# --8<-- [end:forecast]


def main() -> None:
# --8<-- [start:table]
    rng = random.Random(14)
    truth = spin_up()
    print(" lead   spread   error of   error of")
    print("                 the mean    one run")
    for lead, sp, e_mean, e_one in forecast(truth, rng, range(0, 161, 20)):
        print(f"{lead:5.1f}  {sp:7.2f}  {e_mean:9.2f}  {e_one:9.2f}")
# --8<-- [end:table]


if __name__ == "__main__":
    main()
