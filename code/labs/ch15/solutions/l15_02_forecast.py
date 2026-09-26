"""Reference solution for Lab 15.2."""


def nearest(library: list[float], x: float, count: int,
            h: int) -> list[int]:
    """The `count` positions closest to x that have a value h steps on."""
    positions = range(len(library) - h)
    return sorted(positions, key=lambda j: abs(library[j] - x))[:count]


def forecast(library: list[float], x: float, h: int,
             count: int = 1) -> float:
    """The average of library[j + h] over the `count` nearest positions."""
    js = nearest(library, x, count, h)
    return sum(library[j + h] for j in js) / len(js)


def mean_error(xs: list[float], h: int, split: int,
               count: int = 1) -> float:
    """The average miss h steps ahead, learning from xs[:split]."""
    library, test = xs[:split], xs[split:]
    misses = [abs(forecast(library, test[t], h, count) - test[t + h])
              for t in range(len(test) - h)]
    return sum(misses) / len(misses)
