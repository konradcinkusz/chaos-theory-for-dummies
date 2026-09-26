"""Chapter 1's plots: two models, and an error that dies away."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch01"))

from _style import AMBER, BLUE, GREY, T, main, new, plot
from cooling_cup import ROOM, next_minute
from falling_stone import distance


def _tea(start: float, minutes: int) -> list[float]:
    temps = [start]
    for _ in range(minutes):
        temps.append(next_minute(temps[-1]))
    return temps


@plot("ch01-two-models")
def two_models(lang: str):
    fig, (left, right) = new(height=2.6, ncols=2)
    ts = [i / 20 for i in range(101)]
    left.plot(ts, [distance(t) for t in ts], color=BLUE)
    left.set_xlabel(T(lang, "time since release (s)",
                      "czas od puszczenia (s)"))
    left.set_ylabel(T(lang, "distance fallen (m)", "przebyta droga (m)"))
    left.set_title(T(lang, "A stone, from a formula", "Kamień: ze wzoru"))
    temps = _tea(90.0, 60)
    right.plot(range(61), temps, "o", ms=2, color=AMBER)
    right.axhline(ROOM, color=GREY, lw=0.6, ls="--")
    right.set_xlabel(T(lang, "minute", "minuta"))
    right.set_ylabel(T(lang, "temperature (°C)", "temperatura (°C)"))
    right.set_title(T(lang, "Tea, one step at a time",
                      "Herbata: krok po kroku"))
    fig.tight_layout()
    return fig


@plot("ch01-gap-shrinks")
def gap_shrinks(lang: str):
    fig, ax = new(height=2.4)
    a, b = _tea(90.0, 60), _tea(91.0, 60)
    ax.semilogy(range(61), [y - x for x, y in zip(a, b, strict=True)],
                "o", ms=2.5, color=BLUE)
    ax.set_xlabel(T(lang, "minute", "minuta"))
    ax.set_ylabel(T(lang, "gap between the cups (°C)",
                    "różnica między kubkami (°C)"))
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    main()
