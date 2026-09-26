from labs._loader import load


def test_distance_matches_the_table() -> None:
    lab = load("ch01", "l01_01_stone")
    assert abs(lab.distance(2) - 19.62) < 1e-9
    assert abs(lab.distance(3, g=1.62) - 7.29) < 1e-9   # on the Moon


def test_fall_time_undoes_distance() -> None:
    lab = load("ch01", "l01_01_stone")
    for t in (0.5, 1.0, 2.0, 4.5):
        assert abs(lab.fall_time(lab.distance(t)) - t) < 1e-12


def test_a_measured_drop_gives_back_gravity() -> None:
    lab = load("ch01", "l01_01_stone")
    # a stone dropped from 10 m and timed at 1.43 s
    assert abs(lab.estimate_g(10, 1.43) - 9.78) < 0.01
    assert abs(lab.estimate_g(lab.distance(2.5), 2.5) - 9.81) < 1e-12
