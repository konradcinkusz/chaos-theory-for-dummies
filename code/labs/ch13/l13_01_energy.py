"""Lab 13.1 -- the double pendulum's energy, the number that must not move.

The pendulum of the chapter: arms 1 m long, bobs of 1 kg, g = 9.81. A state
is four numbers (upper, lower, upper_speed, lower_speed): the two angles in
radians, measured from hanging straight down, and how fast each is changing
in radians a second.

Potential energy is g times each bob's height, measured upwards from the
pivot, so a bob hanging below the pivot has a negative height. The upper bob
is at height -cos(upper); the lower bob is one arm further down, at
-cos(upper) - cos(lower).

Kinetic energy is half of each bob's speed squared. The upper bob moves at
speed upper_speed (a one-metre arm turning at that rate). The lower bob is
carried by the upper one and swings as well: two arrows added, of lengths
upper_speed and lower_speed, at the angle (upper - lower) to each other. So
its speed squared is

    upper_speed**2 + lower_speed**2
    + 2 * upper_speed * lower_speed * cos(upper - lower)
"""

G = 9.81


def heights(state: tuple[float, ...]) -> tuple[float, float]:
    """The heights of the upper and lower bob above the pivot, in metres."""
    raise NotImplementedError("your turn: replace this line")


def energy(state: tuple[float, ...]) -> float:
    """Kinetic plus potential energy of the pendulum, in joules."""
    raise NotImplementedError("your turn: replace this line")
