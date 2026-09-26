"""Chapter 15 -- an epidemic with a school year.

The SIR model: s is the fraction of people who can still catch the disease
(susceptible), i the fraction who have it (infectious); everyone else has
recovered. Each step, new infections are beta * s * i, an infectious
person recovers after DAYS_ILL days on average, and births bring in new
susceptibles as deaths remove people. The contact rate beta rises and falls
once a year with the school year, by a fraction called the season.

Only +, -, * and / in the loop, so every machine prints the same years.
"""
# transcript: ch15-epidemic

R0 = 17.0            # cases one case causes when nobody is immune
DAYS_ILL = 13.0      # days a case stays infectious, on average
LIFE = 50 * 365.0    # average lifetime in days; births replace deaths
STEPS = 4            # steps per day
YEARS = 400          # years run before the last few are printed
SEASONS = (0.0, 0.1, 0.3, 0.4)   # the strengths of the school year tried


# --8<-- [start:rule]
def contact(day: int, season: float) -> float:
    """How much above or below average the contact rate is on this day:
    1 + season on New Year's Day, 1 - season at midsummer, in straight
    lines between."""
    return 1.0 + season * (4.0 * abs(day / 365.0 - 0.5) - 1.0)


def one_year(s: float, i: float,
             season: float) -> tuple[float, float, float]:
    """Step through one year; return the new s and i, and the fraction
    of people infected during the year."""
    births, recover, dt = 1.0 / LIFE, 1.0 / DAYS_ILL, 1.0 / STEPS
    beta0 = R0 * (recover + births)
    cases = 0.0
    for day in range(365):
        beta = beta0 * contact(day, season)
        for _ in range(STEPS):
            new = beta * s * i
            s = s + dt * (births - new - births * s)
            i = i + dt * (new - (recover + births) * i)
            cases = cases + dt * new
    return s, i, cases
# --8<-- [end:rule]


def yearly_cases(season: float, s: float = 0.06, i: float = 0.001,
                 years: int = YEARS, keep: int = 8) -> list[float]:
    """Cases per thousand people in each of the last `keep` years."""
    out = []
    for year in range(years):
        s, i, cases = one_year(s, i, season)
        if year >= years - keep:
            out.append(1000.0 * cases)
    return out


def main() -> None:
    print("season  cases per thousand people, eight years running")
    for season in SEASONS:
        years = yearly_cases(season)
        print(f"{season:6.1f}  " + " ".join(f"{c:4.0f}" for c in years))
    print("the same, starting one part in a billion more susceptible:")
    for season in (SEASONS[1], SEASONS[-1]):
        years = yearly_cases(season, s=0.06 + 1e-9)
        print(f"{season:6.1f}  " + " ".join(f"{c:4.0f}" for c in years))


if __name__ == "__main__":
    main()
