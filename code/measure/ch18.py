"""Chapter 18's numbers: horizons, what a thousandfold better measurement
buys, and what an ensemble still knows after the horizon.

Every value comes from the same functions the chapter's listings print
(code/ch18/), so the page and the listings cannot disagree. The trajectories
use only + - * / and sqrt; a logarithm is only ever applied to a number that
is already determined, or summed into an average printed to three decimals,
so nothing here can move by a digit between machines.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch18"))

from _exponents import henon_exponent, logistic_exponent, lorenz_exponent
from _values import Values
from beyond import MEMBERS, long_run, odds
from horizon import forecast_length
from thousandfold import STARTS, typical_horizon

v = Values("ch18")


def printed(x: float, fmt: str) -> float:
    """The number a reader sees on the page, read back as a number."""
    return float(format(x, fmt))


# The three exponents the horizon table is built from.
lam = logistic_exponent()
lam_henon = henon_exponent()
lam_lorenz = lorenz_exponent()
assert abs(lam - math.log(2)) < 0.005, "the logistic map at r = 4: ln 2"
v.num("lam.logistic", lam, ".3f")
v.num("lam.henon", lam_henon, ".3f")
v.num("lam.lorenz", lam_lorenz, ".3f")

# The worked horizon: start right to six digits, tolerance 0.1.
ln_six = math.log(0.1 / (1 / 10**6))
six, nine = forecast_length(lam, 6), forecast_length(lam, 9)
v.num("ln.six", ln_six, ".3f")
v.num("hor.six", six, ".1f")
v.num("hor.nine", nine, ".1f")
# The page divides the two printed numbers; they must give the printed answer.
assert format(printed(ln_six, ".3f") / printed(lam, ".3f"), ".1f") == \
    format(six, ".1f")

# A thousandfold better start buys ln(1000)/lambda steps, not a thousand
# times as many.
v.num("ln.thousand", math.log(1000), ".3f")
v.num("hor.gain", nine - six, ".1f")
assert 9.5 < nine - six < 10.5
assert format(printed(math.log(1000), ".3f") / printed(lam, ".3f"),
              ".1f") == format(nine - six, ".1f")
v.num("per.digit", math.log(10) / lam, ".1f")
v.num("per.digit.henon", math.log(10) / lam_henon, ".1f")
assert lam_henon < lam, "the Henon map's errors grow more slowly"

# The same question answered the long way, on the map itself.
apart_six = typical_horizon(1 / 10**6)
apart_nine = typical_horizon(1 / 10**9)
assert apart_six == int(apart_six) and apart_nine == int(apart_nine)
v.num("apart.starts", len(STARTS))
v.num("apart.six", int(apart_six))
v.num("apart.nine", int(apart_nine))
v.num("apart.gain", int(apart_nine - apart_six))
assert abs((apart_nine - apart_six) - (nine - six)) <= 1

# The planets: a Lyapunov time of about five million years (Laskar, 1989,
# as quoted in Chapter 13), an error of one metre, and a tolerance the size
# of the Earth's orbit, 150 million km.
LYAPUNOV_TIME_MYR = 5
ORBIT_M = 1.5e11
ln_planets = math.log(ORBIT_M / 1.0)
planets = LYAPUNOV_TIME_MYR * ln_planets
planets_gain = LYAPUNOV_TIME_MYR * math.log(1000)
v.num("planets.ln", ln_planets, ".1f")
v.num("planets.hor", int(round(planets, -1)))
v.num("planets.gain", round(planets_gain))
assert 100 < planets < 150 and 30 < planets_gain < 40

# The ensemble: how long all the runs agree, and what the odds settle to.
wide, narrow = odds(0.3, 1e-6, 45), odds(0.3, 1e-9, 45)


def last_unanimous(fractions: list[float]) -> int:
    """The last step up to which every run agreed (odds of 0 or 1)."""
    n = 0
    while fractions[n + 1] in (0.0, 1.0):
        n += 1
    return n


sure_six, sure_nine = last_unanimous(wide), last_unanimous(narrow)
v.num("ens.members", MEMBERS)
v.num("ens.sure.six", sure_six)
v.num("ens.sure.nine", sure_nine)
assert 7 <= sure_nine - sure_six <= 12
climate = long_run(0.3)
assert format(climate, ".2f") == format(long_run(0.8), ".2f") == "0.33"
v.num("ens.clim", climate, ".2f")
assert all(abs(p - 1 / 3) < 0.05 for p in wide[30:]), "odds settle to a third"

v.write()
