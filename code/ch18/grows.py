"""Chapter 18 -- the first question of the field guide: run it twice.

Three rules, each started twice from states a billionth apart. Watch what
happens to the gap. Nothing here needs more than + - * and /, so every digit
printed is the same on every machine.
"""
# transcript: ch18-grows

from chaoslab import logistic


def tea(temp: float) -> float:
    """Chapter 1's cooling cup: lose a tenth of the gap to a 20 C room."""
    return temp - 0.1 * (temp - 20.0)


RULES = [("cooling tea", tea, 90.0),
         ("logistic, r = 2.8", logistic(2.8), 0.3),
         ("logistic, r = 4", logistic(4.0), 0.3)]


def main() -> None:
# --8<-- [start:twice]
    print("gap after step:      0        10        20        30        40")
    for name, rule, start in RULES:
        a, b = start, start + 1e-9      # two starts a billionth apart
        gaps = []
        for step in range(41):
            if step % 10 == 0:
                gaps.append(f"{abs(b - a):8.1e}")
            a, b = rule(a), rule(b)
        print(f"{name:18s}" + "  ".join(gaps))
# --8<-- [end:twice]


if __name__ == "__main__":
    main()
