"""Lab 7.2 -- how far ahead a prediction is good for.

An error of size delta grows, on average, by the factor e**lam per step,
where lam is the Lyapunov exponent. Write three functions:

  horizon       steps until the error reaches the tolerance tol;
  extra_steps   how many MORE steps you get by making the error
                `factor` times smaller;
  digits_needed the smallest whole number of decimal places the start
                must be measured to, for the error to stay under tol for
                `steps` steps. (An error of 10**-d means d decimal places.)

Python's math.log is the natural logarithm; math.log10 is base ten, and
math.ceil rounds up to a whole number.
"""


def horizon(lam: float, delta: float, tol: float) -> float:
    """Steps until an error delta grows to tol, at lam per step."""
    raise NotImplementedError("your turn: replace this line")


def extra_steps(lam: float, factor: float) -> float:
    """Steps gained by measuring the start `factor` times more precisely."""
    raise NotImplementedError("your turn: replace this line")


def digits_needed(lam: float, steps: int, tol: float) -> int:
    """Decimal places of the start needed to stay under tol for `steps`."""
    raise NotImplementedError("your turn: replace this line")
