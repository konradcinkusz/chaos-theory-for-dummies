"""Chapter 2's plots: three fates, two accounts, and cobwebs on a line."""

from __future__ import annotations

from _style import AMBER, BLUE, GREY, RED, TEAL, T, main, new, num, plot

from chaoslab import cobweb, linear, orbit


@plot("ch02-three-fates")
def three_fates(lang: str):
    fig, (grow, shrink, settle) = new(height=2.4, ncols=3)
    ns = range(13)
    grow.plot(ns, orbit(linear(2.0, 0.0), 1.0, 12), "o-", ms=2.5,
              color=RED)
    grow.set_title(T(lang, "$x \\mapsto 2x$: grows",
                     "$x \\mapsto 2x$: rośnie"))
    shrink.plot(ns, orbit(linear(0.5, 0.0), 1.0, 12), "o-", ms=2.5,
                color=BLUE)
    shrink.set_title(T(lang, "$x \\mapsto 0.5x$: dies away",
                       "$x \\mapsto 0{,}5x$: zanika"))
    settle.axhline(10.0, color=GREY, lw=0.6, ls="--")
    settle.plot(ns, orbit(linear(0.5, 5.0), 1.0, 12), "o-", ms=2.5,
                color=TEAL, label="$0.5x + 5$" if lang == "en"
                else "$0{,}5x + 5$")
    settle.plot(ns, orbit(linear(-0.5, 15.0), 1.0, 12), "o-", ms=2.5,
                color=AMBER, label="$-0.5x + 15$" if lang == "en"
                else "$-0{,}5x + 15$")
    settle.set_title(T(lang, "two rules that settle",
                       "dwie reguły, które się ustalają"))
    settle.legend(frameon=False, loc="lower right")
    for ax in (grow, shrink, settle):
        ax.set_xlabel(T(lang, "step $n$", "krok $n$"))
    grow.set_ylabel("$x_n$")
    fig.tight_layout()
    return fig


@plot("ch02-two-accounts")
def two_accounts(lang: str):
    fig, ax = new(height=2.5)
    years = range(121)
    adds = orbit(linear(1.0, 50.0), 1000.0, 120)
    grows = orbit(linear(1.02, 0.0), 1000.0, 120)
    cross = next(n for n in years if grows[n] > adds[n])
    ax.plot(years, adds, color=BLUE, lw=1.4,
            label=T(lang, "adds 50 a year", "dopisuje 50 rocznie"))
    ax.plot(years, grows, color=RED, lw=1.4,
            label=T(lang, "grows 2 per cent a year",
                    "rośnie o 2 procent rocznie"))
    ax.axvline(cross, color=GREY, lw=0.6, ls=":")
    ax.annotate(T(lang, f"overtakes in year {cross}",
                  f"wyprzedza w roku {cross}"),
                xy=(cross, adds[cross]), xytext=(cross - 58, 8000),
                arrowprops={"arrowstyle": "->", "color": GREY, "lw": 0.6})
    ax.set_xlabel(T(lang, "years", "lata"))
    ax.set_ylabel(T(lang, "balance", "stan konta"))
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    return fig


def _web(ax, a: float, b: float, x0: float, n: int, lo: float,
         hi: float, colour: str) -> None:
    rule = linear(a, b)
    ax.plot([lo, hi], [lo, hi], color=GREY, lw=0.6)
    ax.plot([lo, hi], [rule(lo), rule(hi)], color=colour, lw=1.2)
    pts = cobweb(rule, x0, n)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color="black",
            lw=0.7)
    ax.plot([200.0], [200.0], "o", ms=3.5, color=colour)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_aspect("equal")
    ax.set_xlabel("$x_n$")


def _slope(lang: str, a: float) -> str:
    """A slope for a title, with a true minus sign and the decimal marker."""
    return num(lang, a, ".1f").replace("-", "\u2212")


@plot("ch02-cobweb")
def cobwebs(lang: str):
    fig, (left, mid, right) = new(height=2.8, ncols=3)
    _web(left, 0.5, 100.0, 20.0, 8, 0.0, 300.0, BLUE)
    _web(mid, -0.5, 300.0, 20.0, 12, 0.0, 300.0, AMBER)
    _web(right, 1.5, -100.0, 190.0, 6, 0.0, 300.0, RED)
    shapes = (T(lang, "staircase in", "schodki do środka"),
              T(lang, "web winds in", "pajęczyna do środka"),
              T(lang, "staircase out", "schodki na zewnątrz"))
    word = T(lang, "slope", "nachylenie")
    for ax, a, shape in zip((left, mid, right), (0.5, -0.5, 1.5), shapes,
                            strict=True):
        ax.set_title(f"{word} {_slope(lang, a)}\n{shape}")
    left.set_ylabel("$x_{n+1}$")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
