"""Chapter 8's plots: the bifurcation diagram, the ratios converging for two
maps, and a zoom into the period-three window.

Plots are not gated by `make verify`, so numpy is used here for speed where
thousands of values of r are run side by side; the rule is the same one the
listings print, x -> r*x*(1 - x), applied to a whole column of r at once.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch08"))

from _style import AMBER, BLUE, GREY, T, main, new, num, plot
from superstable import LOGISTIC, landmarks, ratios
from two_maps import SINE


def _cloud(r_lo: float, r_hi: float, columns: int, burn: int,
           keep: int) -> tuple[np.ndarray, np.ndarray]:
    """For `columns` values of r, the `keep` values after `burn` steps."""
    r = np.linspace(r_lo, r_hi, columns)
    x = np.full(columns, 0.5)
    for _ in range(burn):
        x = r * x * (1.0 - x)
    rs, xs = [], []
    for _ in range(keep):
        x = r * x * (1.0 - x)
        rs.append(r)
        xs.append(x.copy())
    return np.concatenate(rs), np.concatenate(xs)


def _dots(ax, r, x) -> None:
    ax.plot(r, x, ",", color=BLUE, alpha=0.35, rasterized=True)


@plot("ch08-diagram")
def diagram(lang: str):
    fig, ax = new(height=3.4)
    r, x = _cloud(2.8, 4.0, 2400, 1000, 300)
    _dots(ax, r, x)
    ax.set_xlim(2.8, 4.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel(T(lang, "the knob r", "pokrętło r"))
    ax.set_ylabel(T(lang, "where x lives in the long run",
                    "gdzie x przebywa na dłuższą metę"))
    fig.tight_layout()
    return fig


@plot("ch08-ratios")
def ratio_plot(lang: str):
    fig, ax = new(height=2.5)
    a = ratios(landmarks(*LOGISTIC, count=11))
    b = ratios(landmarks(*SINE, count=11))
    ns = list(range(2, 2 + len(a)))
    ax.axhline(a[-1], color=GREY, lw=0.6, ls="--")
    ax.plot(ns, a, "o-", ms=3.5, color=BLUE,
            label=T(lang, r"logistic map  $r\,x\,(1-x)$",
                    r"odwzorowanie logistyczne  $r\,x\,(1-x)$"))
    ax.plot(ns, b, "s-", ms=3.5, color=AMBER,
            label=T(lang, r"sine map  $s\,\sin(\pi x)$",
                    r"odwzorowanie sinusowe  $s\,\sin(\pi x)$"))
    ax.text(ns[-1], a[-1] + 0.02, num(lang, a[-1], ".4f"),
            ha="right", va="bottom", color=GREY, fontsize=8)
    ax.set_xlabel(T(lang, "landmark n", "punkt n"))
    ax.set_ylabel(T(lang, "gap before n / gap after n",
                    "luka przed n / luka po n"))
    ax.set_xticks(ns)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    return fig


@plot("ch08-zoom")
def zoom(lang: str):
    fig, (left, right) = new(height=2.8, ncols=2)
    r, x = _cloud(3.82, 3.86, 1200, 3000, 400)
    _dots(left, r, x)
    left.set_xlim(3.82, 3.86)
    left.set_ylim(0.0, 1.0)
    box = (3.8400, 3.8575, 0.44, 0.56)
    left.add_patch(Rectangle(
        (box[0], box[2]), box[1] - box[0], box[3] - box[2],
        fill=False, lw=0.7, color=AMBER))
    near = num(lang, 3.83, ".2f")
    left.set_title(T(lang, f"The window near r = {near}",
                     f"Okno w pobliżu r = {near}"))
    r, x = _cloud(box[0], box[1], 1200, 3000, 600)
    _dots(right, r, x)
    right.set_xlim(box[0], box[1])
    right.set_ylim(box[2], box[3])
    right.set_title(T(lang, "Its middle, magnified",
                      "Jego środek w powiększeniu"))
    for ax in (left, right):
        ax.set_xlabel("r")
    left.set_ylabel("x")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
