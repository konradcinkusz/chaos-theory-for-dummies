"""Reference solution for Lab 8.2."""


def ratios(landmarks: list[float]) -> list[float]:
    """Each gap divided by the next one."""
    gaps = [b - a for a, b in zip(landmarks, landmarks[1:], strict=False)]
    return [g / h for g, h in zip(gaps, gaps[1:], strict=False)]


def where_it_ends(landmarks: list[float]) -> float:
    """The last landmark plus every gap still to come."""
    d = ratios(landmarks)[-1]
    g = landmarks[-1] - landmarks[-2]
    return landmarks[-1] + g / (d - 1)
