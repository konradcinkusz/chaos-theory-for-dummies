"""Chapter 3's plots: doubling against crowding, a curve that looks
straight when you zoom in, and the overshoot."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch03"))

from _style import AMBER, BLUE, GREY, TEAL, T, main, new, num, plot
from crowding import next_gen
from overshoot import in_instalments
from settle import slope_at


@plot("ch03-s-curve")
def s_curve(lang: str):
    fig, ax = new(height=2.6)
    gens = range(16)
    free, crowded = [0.001], [0.001]
    for _ in gens[1:]:
        free.append(2.0 * free[-1])
        crowded.append(next_gen(crowded[-1], 2.0))
    ax.plot(gens, free, "o-", ms=3, color=AMBER,
            label=T(lang, "doubling, room ignored",
                    "podwajanie, bez względu na miejsce"))
    ax.plot(gens, crowded, "o-", ms=3, color=BLUE,
            label=T(lang, "doubling, room running out",
                    "podwajanie, gdy brakuje miejsca"))
    ax.axhline(1.0, color=GREY, lw=0.6, ls="--")
    ax.text(0.2, 1.02, T(lang, "the whole room", "całe miejsce"),
            color=GREY, fontsize=8, va="bottom")
    ax.set_ylim(0, 1.2)
    ax.set_xlim(-0.3, 15.3)
    ax.set_xlabel(T(lang, "generation", "pokolenie"))
    ax.set_ylabel(T(lang, "population (fraction of the room)",
                    "populacja (ułamek miejsca)"))
    ax.legend(loc="center right", frameon=False)
    fig.tight_layout()
    return fig


@plot("ch03-zoom")
def zoom(lang: str):
    fig, axes = new(height=2.4, ncols=3)
    r = 1.5
    fixed = 1 - 1 / r
    s = slope_at(fixed, r)
    titles = (T(lang, "the whole rule", "cała reguła"),
              T(lang, "ten times closer", "dziesięć razy bliżej"),
              T(lang, "a hundred times closer", "sto razy bliżej"))
    for ax, half, title in zip(axes, (0.5, 0.05, 0.005), titles,
                               strict=True):
        lo, hi = fixed - half, fixed + half
        if half == 0.5:
            lo, hi = 0.0, 1.0
        xs = [lo + (hi - lo) * i / 200 for i in range(201)]
        ax.plot(xs, [next_gen(x, r) for x in xs], color=BLUE,
                label=T(lang, "the rule", "reguła"))
        near = [x for x in xs if abs(x - fixed) <= min(half, 0.2)]
        ax.plot(near, [fixed + s * (x - fixed) for x in near], color=AMBER,
                ls="--", lw=0.9,
                label=T(lang, "straight line, slope ",
                        "prosta o nachyleniu ") + num(lang, s, ".1f"))
        ax.plot([fixed], [fixed], "o", ms=4, color=TEAL)
        ax.set_xlim(lo, hi)
        ax.set_title(title)
        ax.set_xlabel(T(lang, "this generation", "to pokolenie"))
        ax.locator_params(nbins=3)
    axes[0].set_ylabel(T(lang, "next generation", "następne pokolenie"))
    axes[0].set_ylim(0, 0.45)
    axes[0].legend(loc="lower center", frameon=False, fontsize=7)
    fig.tight_layout()
    return fig


@plot("ch03-overshoot")
def overshoot(lang: str):
    fig, ax = new(height=2.6)
    r = 2.8
    once, paid = [0.01], [0.01]
    for _ in range(25):
        once.append(next_gen(once[-1], r))
        paid.append(in_instalments(paid[-1], r))
    gens = range(26)
    ax.axhline(1 - 1 / r, color=GREY, lw=0.6, ls="--")
    ax.text(25.2, 1 - 1 / r + 0.012,
            T(lang, "settled level", "poziom ustalony"),
            color=GREY, fontsize=8, ha="right", va="bottom")
    ax.plot(gens, once, "o-", ms=3, color=BLUE,
            label=T(lang, "once a generation", "raz na pokolenie"))
    ax.plot(gens, paid, "s-", ms=2.5, color=AMBER,
            label=T(lang, "in ten instalments", "w dziesięciu ratach"))
    ax.set_ylim(0, 0.8)
    ax.set_xlabel(T(lang, "generation", "pokolenie"))
    ax.set_ylabel(T(lang, "population", "populacja"))
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
