"""Lab 1.1 -- the falling stone, both ways round.

A model answers questions in more than one direction. Given the time you can
ask for the distance; given the distance you can ask for the time; and given
a measured drop you can ask the model what gravity must be. Write all three.
Air is ignored throughout, as it is in the chapter.
"""

G = 9.81


def distance(t: float, g: float = G) -> float:
    """Metres fallen after t seconds."""
    raise NotImplementedError("your turn: replace this line")


def fall_time(height: float, g: float = G) -> float:
    """Seconds to fall `height` metres. Undo the formula for distance."""
    raise NotImplementedError("your turn: replace this line")


def estimate_g(height: float, seconds: float) -> float:
    """The g that would make a stone fall `height` metres in `seconds`."""
    raise NotImplementedError("your turn: replace this line")
