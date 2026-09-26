"""Chapter 4's plots: Euler against RK4 on a spring, the map of every state
of a pendulum, and two ways for motion in a plane to settle."""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch04"))

import numpy as np
from _settle import van_der_pol
from _style import AMBER, BLUE, GREY, RED, TEAL, T, main, new, plot

from chaoslab import euler_step, integrate, pendulum, rk4_step, spring

G_OVER_L = 9.81
DEG = 180.0 / math.pi


def _energy(s: tuple[float, ...]) -> float:
    return 0.5 * s[1] * s[1] + 0.5 * s[0] * s[0]


@plot("ch04-euler-rk4")
def euler_rk4(lang: str):
    fig, (left, right) = new(height=2.7, ncols=2)
    field = spring(1.0)
    euler = integrate(field, (1.0, 0.0), 0.1, 100, euler_step)
    rk4 = integrate(field, (1.0, 0.0), 0.1, 100, rk4_step)
    angle = np.linspace(0.0, 2 * math.pi, 200)
    left.plot(np.cos(angle), np.sin(angle), color=GREY, lw=0.8, ls="--")
    left.plot([s[0] for s in euler], [s[1] for s in euler], "-o", ms=1.6,
              lw=0.6, color=RED)
    left.plot([s[0] for s in rk4], [s[1] for s in rk4], "o", ms=2.2,
              color=BLUE)
    left.plot([1.0], [0.0], "k*", ms=6)
    left.set_aspect("equal")
    left.set_xlabel(T(lang, "position x (m)", "położenie x (m)"))
    left.set_ylabel(T(lang, "velocity v (m/s)", "prędkość v (m/s)"))
    left.set_title(T(lang, "Ten seconds in the state plane",
                     "Dziesięć sekund na płaszczyźnie stanów"))
    ts = [0.1 * n for n in range(101)]
    fine = integrate(field, (1.0, 0.0), 0.01, 1000, euler_step)[::10]
    right.axhline(0.5, color=GREY, lw=0.8, ls="--",
                  label=T(lang, "the real spring", "prawdziwa sprężyna"))
    right.plot(ts, [_energy(s) for s in euler], color=RED,
               label=T(lang, "Euler, step 0.1 s", "Euler, krok 0,1 s"))
    right.plot(ts, [_energy(s) for s in fine], color=AMBER,
               label=T(lang, "Euler, step 0.01 s", "Euler, krok 0,01 s"))
    right.plot(ts, [_energy(s) for s in rk4], color=BLUE,
               label=T(lang, "RK4, step 0.1 s", "RK4, krok 0,1 s"))
    right.set_ylim(0.0, 1.5)
    right.set_xlabel(T(lang, "time (s)", "czas (s)"))
    right.set_ylabel(T(lang, "energy", "energia"))
    right.set_title(T(lang, "Energy should stay at 0.5",
                      "Energia powinna zostać na 0,5"))
    right.legend(loc="upper left", frameon=False, fontsize=7)
    fig.tight_layout()
    return fig


def _pend_path(theta: float, omega: float, seconds: float,
               damping: float = 0.0) -> list[tuple[float, float]]:
    field = pendulum(G_OVER_L, damping)
    path = integrate(field, (theta, omega), 0.005, round(seconds / 0.005))
    return [(s[0] * DEG, s[1] * DEG) for s in path]


@plot("ch04-pendulum-map")
def pendulum_map(lang: str):
    fig, ax = new(height=3.3)
    th = np.linspace(-200, 200, 25)
    om = np.linspace(-500, 500, 17)
    tt, oo = np.meshgrid(th, om)
    dth = oo
    dom = -G_OVER_L * np.sin(tt / DEG) * DEG
    # arrows of one length: the map shows which way, not how fast
    size = np.hypot(dth / 400.0, dom / 400.0) + 1e-12
    ax.quiver(tt, oo, dth / 400.0 / size, dom / 400.0 / size, color=GREY,
              alpha=0.45, angles="xy", scale=42, width=0.0022)
    period = 2 * math.pi / math.sqrt(G_OVER_L)
    for swing in (30, 90, 150):
        path = _pend_path(math.radians(swing), 0.0, 2.4 * period)
        ax.plot([p[0] for p in path], [p[1] for p in path], color=BLUE,
                lw=1.0)
    edge = 2 * math.sqrt(G_OVER_L)             # just enough to reach the top
    for sign in (1, -1):
        path = _pend_path(-sign * math.radians(200), sign * 4.574, 3.0)
        pts = [p for p in path if -205 < p[0] < 205]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=TEAL,
                lw=1.0)
    th2 = np.linspace(-180, 180, 300)
    for sign in (1, -1):
        ax.plot(th2, sign * edge * np.cos(th2 / DEG / 2) * DEG, color=AMBER,
                lw=0.9, ls="--")
    ax.plot([0], [0], "o", ms=5, color="k")
    ax.plot([-180, 180], [0, 0], "o", ms=5, mfc="white", mec="k")
    ax.set_xlim(-205, 205)
    ax.set_ylim(-520, 520)
    ax.set_xticks([-180, -90, 0, 90, 180])
    ax.set_xlabel(T(lang, "angle from hanging straight down (degrees)",
                    "kąt od pionu w dół (stopnie)"))
    ax.set_ylabel(T(lang, "how fast the angle changes (degrees/s)",
                    "szybkość zmiany kąta (stopnie/s)"))
    ax.text(0, 150, T(lang, "swinging", "wahanie"), ha="center",
            fontsize=8, color=BLUE)
    ax.text(0, 470, T(lang, "going over the top", "obrót przez górę"),
            ha="center", fontsize=8, color=TEAL)
    fig.tight_layout()
    return fig


@plot("ch04-settle")
def settle(lang: str):
    fig, (left, right) = new(height=2.8, ncols=2)
    path = _pend_path(math.radians(150), 0.0, 25.0, damping=0.5)
    left.plot([p[0] for p in path], [p[1] for p in path], color=BLUE,
              lw=0.8)
    left.plot([path[0][0]], [path[0][1]], "k*", ms=6)
    left.plot([0], [0], "o", ms=4, color="k")
    left.set_xlabel(T(lang, "angle (degrees)", "kąt (stopnie)"))
    left.set_ylabel(T(lang, "degrees per second", "stopnie na sekundę"))
    left.set_title(T(lang, "With friction: onto a point",
                     "Z tarciem: do punktu"))
    loop = van_der_pol()
    for start, colour in (((0.1, 0.0), BLUE), ((4.0, 0.0), AMBER)):
        p = integrate(loop, start, 0.01, 6000)
        right.plot([s[0] for s in p], [s[1] for s in p], color=colour,
                   lw=0.7)
        right.plot([start[0]], [start[1]], "*", ms=6, color="k")
    right.set_xlabel("x")
    right.set_ylabel("v")
    right.set_title(T(lang, "Pushed and braked: onto a loop",
                      "Popychane i hamowane: na pętlę"))
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
