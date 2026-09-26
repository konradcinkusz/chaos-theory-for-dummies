"""The plot pipeline: one style, two languages, one registry.

A chapter's plots live in plots/chNN.py, each a function decorated with the
key the book places it under:

    from _style import T, main, new, plot

    @plot("ch05-four-rates")
    def four_rates(lang):
        fig, ax = new()
        ax.plot(...)
        ax.set_xlabel(T(lang, "step n", "krok n"))
        return fig

    if __name__ == "__main__":
        main()

Running the file draws every registered plot twice, into
figures/plots/en/<key>.pdf and figures/plots/pl/<key>.pdf. The key must
appear literally in the decorator: tools/check_structure.py --plots reads it
there to prove every \\plotfig on the page has a script behind it.

The Polish edition gets a decimal COMMA on its tick labels, applied here
once rather than remembered in every script. Numbers written into a label
or a title must go through num(), which does the same.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.ticker import ScalarFormatter  # noqa: E402

CODE = Path(__file__).resolve().parents[1]
OUT = CODE.parent / "figures" / "plots"
LANGS = ("en", "pl")

# The text block is 14.8 cm wide; a figure drawn at that width is placed at
# scale one, so 9 pt here is 9 pt on the page.
WIDTH_IN = 14.8 / 2.54

# The palette the book's boxes use, so a plot reads as part of the page.
BLUE, TEAL, AMBER, RED, VIOLET, GREEN, GREY = (
    "#1F4E79", "#0E7C7B", "#B26A00", "#9B2C2C", "#7B4397", "#3B7A3B",
    "#5A5A5A")
CYCLE = [BLUE, AMBER, TEAL, RED, VIOLET, GREEN, GREY]

matplotlib.rcParams.update({
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.prop_cycle": matplotlib.cycler(color=CYCLE),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.6,
    "lines.linewidth": 1.0,
    "pdf.fonttype": 42,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.03,
    "axes.unicode_minus": True,
})

Plotter = Callable[[str], Figure]
REGISTRY: list[tuple[str, Plotter]] = []


def plot(key: str) -> Callable[[Plotter], Plotter]:
    """Register a plot under the key the book places it with."""

    def wrap(func: Plotter) -> Plotter:
        REGISTRY.append((key, func))
        return func

    return wrap


def T(lang: str, en: str, pl: str) -> str:  # noqa: N802 -- a label, not a type
    """The string for this edition."""
    return pl if lang == "pl" else en


def num(lang: str, x: float, fmt: str) -> str:
    """Format a number for a label, with the edition's decimal marker."""
    s = format(x, fmt)
    return s.replace(".", ",") if lang == "pl" else s


def new(height: float = 2.8, ncols: int = 1, nrows: int = 1,
        width: float = WIDTH_IN, **kw) -> tuple[Figure, Axes]:
    """A figure the width of the text block: (fig, ax) or (fig, axes)."""
    fig, ax = plt.subplots(nrows, ncols, figsize=(width, height), **kw)
    return fig, ax


class _CommaFormatter(ScalarFormatter):
    """ScalarFormatter with the Polish decimal comma."""

    def __call__(self, x: float, pos: int | None = None) -> str:
        s = super().__call__(x, pos)
        return s.replace(".", "{,}") if "$" in s else s.replace(".", ",")


def _localise(fig: Figure, lang: str) -> None:
    if lang != "pl":
        return
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            fmt = axis.get_major_formatter()
            if type(fmt) is ScalarFormatter:
                new_fmt = _CommaFormatter()
                new_fmt.set_useOffset(fmt.get_useOffset())
                axis.set_major_formatter(new_fmt)


def save(fig: Figure, key: str, lang: str) -> Path:
    path = OUT / lang / f"{key}.pdf"
    path.parent.mkdir(parents=True, exist_ok=True)
    _localise(fig, lang)
    # No creation date, so the same data draws the same bytes.
    fig.savefig(path, metadata={"CreationDate": None, "ModDate": None,
                                "Producer": "chaos-from-zero"})
    plt.close(fig)
    return path


def main() -> int:
    """Draw every plot registered by the calling file, in both languages."""
    only = set(sys.argv[1:])
    for key, func in REGISTRY:
        if only and key not in only:
            continue
        for lang in LANGS:
            save(func(lang), key, lang)
        print(f"  plot: figures/plots/{{en,pl}}/{key}.pdf")
    return 0
