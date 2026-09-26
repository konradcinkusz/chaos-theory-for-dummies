from labs._loader import load


def test_cool_keeps_every_minute() -> None:
    lab = load("ch01", "l01_02_cooling")
    temps = lab.cool(90.0, 20.0, 0.1, 3)
    assert len(temps) == 4
    assert abs(temps[1] - 83.0) < 1e-12
    assert abs(temps[3] - (20 + 70 * 0.9 ** 3)) < 1e-9


def test_tea_approaches_the_room_and_never_passes_it() -> None:
    lab = load("ch01", "l01_02_cooling")
    temps = lab.cool(90.0, 20.0, 0.1, 200)
    assert all(t > 20.0 for t in temps)
    assert temps[-1] - 20.0 < 1e-6


def test_minutes_until_drinkable() -> None:
    lab = load("ch01", "l01_02_cooling")
    assert lab.minutes_until(90.0, 20.0, 0.1, 60.0) == 6
    assert lab.minutes_until(90.0, 20.0, 0.1, 90.5) == 0
