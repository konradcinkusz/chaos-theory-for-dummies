"""Chapter 9 -- the Lyapunov exponent of Lorenz's flow, from three starts.

chaoslab's lyapunov_flow follows two runs a hair apart, adds up how much
their gap grows each step, and pulls the second back after every step so
the gap stays small enough to measure. Then Chapter 7's horizon.
"""
# transcript: ch09-exponent

from chaoslab import horizon, lorenz, lyapunov_flow

STARTS = [(1.0, 1.0, 1.0), (-5.0, 3.0, 20.0), (10.0, -10.0, 30.0)]


def main() -> None:
    # --8<-- [start:exponent]
    field = lorenz()
    for start in STARTS:
        lam = lyapunov_flow(field, start, 0.01, 50_000)  # 500 time units
        print(f"from {start}: {lam:.2f} per time unit")
    # --8<-- [end:exponent]
    # --8<-- [start:horizon]
    t = horizon(0.9, 1e-8, 1.0)     # exponent, error, tolerance
    print(f"horizon from 1e-8 to 1 at 0.9 per time unit: {t:.1f}")
    # --8<-- [end:horizon]


if __name__ == "__main__":
    main()
