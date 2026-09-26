from chaoslab import integrate, lorenz
from labs._loader import load


def test_on_four_states_you_can_check_by_hand() -> None:
    lab = load("ch09", "l09_02_wings")
    path = [(1.0, 0.0, 10.0), (-1.0, 0.0, 20.0), (2.0, 5.0, 30.0),
            (3.0, -5.0, 40.0)]
    assert lab.fraction_right(path) == 0.75
    assert lab.mean_height(path) == 25.0


def test_two_starts_far_apart_give_the_same_summaries() -> None:
    lab = load("ch09", "l09_02_wings")
    field = lorenz()
    near = integrate(field, (1.0, 1.0, 1.0), 0.01, 41_000)[1000:]
    far = integrate(field, (40.0, -40.0, 80.0), 0.01, 41_000)[1000:]
    f1, f2 = lab.fraction_right(near), lab.fraction_right(far)
    h1, h2 = lab.mean_height(near), lab.mean_height(far)
    assert abs(f1 - 0.5) < 0.1 and abs(f2 - 0.5) < 0.1
    assert 23.0 < h1 < 24.0 and 23.0 < h2 < 24.0
    assert abs(h1 - h2) < 0.3
