"""Chapter 11's plots: the Koch curve round by round, what happens to a
measured length as the ruler shrinks, and the box counts on a log-log plot.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch11"))

from _ruler import length
from _style import AMBER, BLUE, GREY, RED, TEAL, T, main, new, plot
from henon_boxes import SIZES as HENON_SIZES
from henon_boxes import attractor
from koch_boxes import POINTS as KOCH_POINTS
from koch_boxes import SIZES as KOCH_SIZES
from koch_boxes import counts, dimension
from matplotlib.patches import Rectangle
from semicircle import rounds

from chaoslab import cantor, koch

HEIGHT = math.sqrt(3.0) / 6.0


@plot("ch11-koch-stages")
def koch_stages(lang: str):
    fig, axes = new(height=2.2, ncols=3, nrows=2)
    for n, ax in enumerate(axes.flat):
        pts = koch(n)
        ax.add_patch(Rectangle((0, 0), 1, HEIGHT, fill=False, ls="--",
                               lw=0.5, ec=GREY))
        ax.plot([x for x, _ in pts], [y for _, y in pts], color=BLUE,
                lw=0.8)
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.03, HEIGHT + 0.03)
        ax.set_aspect("equal")
        ax.axis("off")
        pieces = 4**n
        ax.set_title(T(lang, f"round {n}: {pieces} piece"
                       + ("" if pieces == 1 else "s"),
                       f"runda {n}: {pieces} "
                       + ("odcinek" if pieces == 1 else
                          "odcinki" if pieces == 4 else "odcinków")),
                     fontsize=8)
    fig.tight_layout()
    return fig


@plot("ch11-three-fates")
def three_fates(lang: str):
    fig, ax = new(height=2.7)
    semi = rounds(8)
    ax.loglog([length(p[:2]) for p in semi], [length(p) for p in semi],
              "o-", ms=3, color=TEAL,
              label=T(lang, "half a circle: settles on $\\pi$",
                      "półokrąg: ustala się na $\\pi$"))
    rulers = [1 / 3**n for n in range(8)]
    ax.loglog(rulers, [length(koch(n)) for n in range(8)], "s-", ms=3,
              color=RED, label=T(lang, "Koch curve: grows for ever",
                                 "krzywa Kocha: rośnie bez końca"))
    ax.loglog(rulers, [sum(b - a for a, b in cantor(n)) for n in range(8)],
              "^-", ms=3, color=AMBER,
              label=T(lang, "Cantor set: shrinks to nothing",
                      "zbiór Cantora: kurczy się do zera"))
    ax.invert_xaxis()
    ax.set_xlabel(T(lang, "ruler length (shorter to the right)",
                    "długość linijki (w prawo coraz krótsza)"))
    ax.set_ylabel(T(lang, "measured length", "zmierzona długość"))
    ax.legend(frameon=False, loc="lower left")
    fig.tight_layout()
    return fig


@plot("ch11-box-counts")
def box_counts(lang: str):
    fig, (left, right) = new(height=2.8, ncols=2,
                             gridspec_kw={"width_ratios": [1.1, 1]})
    pts = attractor(20_000)
    s = 1 / 16
    boxes = {(math.floor(x / s), math.floor(y / s)) for x, y in pts}
    for i, j in boxes:
        left.add_patch(Rectangle((i * s, j * s), s, s, lw=0.3,
                                 ec=GREY, fc="#DCE6F0"))
    left.plot([x for x, _ in pts], [y for _, y in pts], ",", color=BLUE)
    left.set_aspect("equal")
    left.set_xlim(-1.4, 1.4)
    left.set_ylim(-0.45, 0.45)
    left.set_title(T(lang, f"{len(boxes)} boxes of side 1/16",
                     f"{len(boxes)} pudełek o boku 1/16"))
    left.set_xlabel("$x$")
    left.set_ylabel("$y$")

    for name, points, sizes, colour, mark in (
            (T(lang, "Koch curve", "krzywa Kocha"), KOCH_POINTS,
             KOCH_SIZES, RED, "s"),
            (T(lang, "H\u00e9non attractor", "atraktor H\u00e9nona"),
             attractor(1_000_000), HENON_SIZES, BLUE, "o")):
        ns = counts(points, sizes)
        d = dimension(sizes, ns)
        xs = [1 / q for q in sizes]
        right.loglog(xs, ns, mark, ms=3, color=colour,
                     label=f"{name}: " + T(lang, "slope", "nachylenie")
                     + f" {d:.2f}".replace(".", "," if lang == "pl"
                                           else "."))
        # the fitted line, drawn through the middle of the points
        mx = sum(math.log(x) for x in xs) / len(xs)
        my = sum(math.log(n) for n in ns) / len(ns)
        ends = [xs[0], xs[-1]]
        right.loglog(ends, [math.exp(my + d * (math.log(x) - mx))
                            for x in ends], color=colour, lw=0.6)
    for slope, label in ((1, T(lang, "slope 1", "nachylenie 1")),
                         (2, T(lang, "slope 2", "nachylenie 2"))):
        right.loglog([2, 1024], [3 * (x / 2) ** slope for x in (2, 1024)],
                     ls="--", lw=0.6, color=GREY)
        right.annotate(label, (1024, 3 * 512**slope), fontsize=7,
                       color=GREY, ha="right", va="bottom")
    right.set_xlabel(T(lang, "boxes per unit length, $1/s$",
                       "pudełek na jednostkę długości, $1/s$"))
    right.set_ylabel(T(lang, "boxes touched, $N$", "zajęte pudełka, $N$"))
    right.legend(frameon=False, loc="upper left", fontsize=7)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
