"""Chapter 11 -- measuring a curve the way a surveyor measures a coast.

Imported by the chapter's listings rather than run on its own. A curve is a
list of points; its measured length is the sum of the straight steps from
each point to the next, which is what you get by walking a ruler along it.
"""

from __future__ import annotations

import math
from itertools import pairwise

Point = tuple[float, float]


# --8<-- [start:length]
def length(points: list[Point]) -> float:
    """Add up the straight steps from each point to the next."""
    total = 0.0
    for (x0, y0), (x1, y1) in pairwise(points):
        dx, dy = x1 - x0, y1 - y0
        total += math.sqrt(dx * dx + dy * dy)   # Pythagoras
    return total
# --8<-- [end:length]
