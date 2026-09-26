"""Chapter 13's plots: two releases parting, the energy check, and the
release angles at which a double pendulum stays calm."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch13"))

from _style import AMBER, BLUE, GREY, RED, TEAL, T, main, new, num, plot
from gentle_wild import SECONDS
from release import DT, RULE, release
from step_check import STEPS, parting
from two_releases import APART, NUDGE, gap

from chaoslab import double_pendulum_energy, rk4_step


@plot("ch13-two-releases")
def two_releases(lang: str):
    fig, (top, bottom) = new(height=3.6, nrows=2, sharex=True)
    a = release(120, 120)
    b = (a[0] + NUDGE, a[1], a[2], a[3])
    ts, la, lb, gaps = [], [], [], []
    for step in range(16_001):
        if step % 20 == 0:
            ts.append(step * DT)
            la.append(math.degrees(a[1]))
            lb.append(math.degrees(b[1]))
            gaps.append(gap(a, b))
        a, b = rk4_step(RULE, a, DT), rk4_step(RULE, b, DT)
    top.plot(ts, la, color=BLUE, label=T(lang, "first release",
                                            "pierwsze puszczenie"))
    top.plot(ts, lb, color=AMBER, ls="--",
             label=T(lang, "a millionth of a radian further round",
                     "o milionową część radiana dalej"))
    top.set_ylabel(T(lang, "lower arm (degrees)", "dolne ramię (stopnie)"))
    top.legend(loc="upper left", frameon=False)
    bottom.semilogy(ts, gaps, color=RED)
    bottom.axhline(APART, color=GREY, lw=0.6, ls="--")
    bottom.text(0.2, APART * 1.6, T(lang, "a gap anyone can see",
                                    "różnica, którą każdy zobaczy"),
                color=GREY, fontsize=8)
    bottom.set_ylabel(T(lang, "gap (radians)", "różnica (radiany)"))
    bottom.set_xlabel(T(lang, "time (s)", "czas (s)"))
    fig.tight_layout()
    return fig


@plot("ch13-energy-error")
def energy_error(lang: str):
    fig, ax = new(height=2.6)
    colours = [GREY, TEAL, BLUE, AMBER]
    for dt, colour in zip(STEPS, colours, strict=True):
        s = release(120, 120)
        e0 = double_pendulum_energy(s)
        ts, errs = [], []
        steps = round(20.0 / dt)
        every = max(1, steps // 400)
        for step in range(1, steps + 1):
            s = rk4_step(RULE, s, dt)
            if step % every == 0:
                ts.append(step * dt)
                errs.append(max(abs(double_pendulum_energy(s) - e0), 1e-16))
        ax.semilogy(ts, errs, color=colour, lw=0.8,
                    label=T(lang, f"step {num(lang, dt, '.4f')} s",
                            f"krok {num(lang, dt, '.4f')} s"))
    apart, _ = parting(DT)
    ax.axvline(apart, color=RED, lw=0.6, ls=":")
    ax.text(apart + 0.2, 1e-3,
            T(lang, "the pair parts", "para się rozchodzi"),
            color=RED, fontsize=8)
    ax.set_xlabel(T(lang, "time (s)", "czas (s)"))
    ax.set_ylabel(T(lang, "change in energy (J)", "zmiana energii (J)"))
    ax.set_ylim(1e-15, 1e-2)
    ax.legend(loc="upper left", frameon=False, ncols=2)
    fig.tight_layout()
    return fig


def _field(s: np.ndarray, g: float = 9.81) -> np.ndarray:
    """chaoslab.double_pendulum's rule for many pendulums at once (arms of
    1 m, bobs of 1 kg), so a whole sweep of releases steps together."""
    t1, t2, w1, w2 = s
    d = t2 - t1
    sd, cd = np.sin(d), np.cos(d)
    den = 2.0 - cd * cd
    a1 = (w1 * w1 * sd * cd + g * np.sin(t2) * cd + w2 * w2 * sd
          - 2.0 * g * np.sin(t1)) / den
    a2 = (-w2 * w2 * sd * cd
          + 2.0 * (g * np.sin(t1) * cd - w1 * w1 * sd - g * np.sin(t2))) / den
    return np.array([w1, w2, a1, a2])


def _rk4(s: np.ndarray, dt: float) -> np.ndarray:
    k1 = _field(s)
    k2 = _field(s + dt / 2 * k1)
    k3 = _field(s + dt / 2 * k2)
    k4 = _field(s + dt * k3)
    return s + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6


@plot("ch13-gentle-wild")
def gentle_wild(lang: str):
    # The vectorised rule must be the library's rule, not a second opinion.
    probe = (0.3, -1.1, 2.0, -0.5)
    assert np.allclose(_field(np.array(probe)), RULE(probe), atol=1e-12)
    angles = np.arange(2.5, 178, 2.5)
    rad = np.radians(angles)
    zero = np.zeros_like(rad)
    a = np.array([rad, rad, zero, zero])
    b = np.array([rad + NUDGE, rad, zero, zero])
    largest = np.abs(b - a)[:2].max(axis=0)
    for _ in range(round(SECONDS / DT)):
        a, b = _rk4(a, DT), _rk4(b, DT)
        largest = np.maximum(largest, np.abs(b - a)[:2].max(axis=0))
    fig, ax = new(height=2.6)
    calm = largest <= APART
    ax.semilogy(angles[calm], largest[calm], "o", ms=3, color=TEAL,
                label=T(lang, "stayed together", "zostały razem"))
    ax.semilogy(angles[~calm], largest[~calm], "o", ms=3, color=RED,
                label=T(lang, "parted", "rozeszły się"))
    ax.axhline(APART, color=GREY, lw=0.6, ls="--")
    ax.set_xlabel(T(lang, "release angle of both arms (degrees)",
                    "kąt puszczenia obu ramion (stopnie)"))
    ax.set_ylabel(T(lang, f"largest gap in {round(SECONDS)} s (rad)",
                    f"największa różnica w {round(SECONDS)} s (rad)"))
    ax.set_xticks(range(0, 181, 30))
    ax.legend(loc="upper left", frameon=False)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
