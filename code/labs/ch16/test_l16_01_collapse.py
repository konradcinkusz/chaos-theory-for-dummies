from labs._loader import load


def test_one_step_doubles_and_drops_the_whole_part() -> None:
    lab = load("ch16", "l16_01_collapse")
    assert lab.doubling(0.25) == 0.5
    assert lab.doubling(0.75) == 0.5
    assert lab.doubling(0.5) == 0.0


def test_the_orbit_of_a_tenth_dies_at_step_55() -> None:
    lab = load("ch16", "l16_01_collapse")
    assert lab.steps_to_zero(0.1) == 55
    assert lab.steps_to_zero(0.75) == 2
    assert lab.steps_to_zero(0.0) == 0


def test_the_prediction_needs_no_running() -> None:
    lab = load("ch16", "l16_01_collapse")
    assert lab.predicted_steps(0.1) == 55
    assert lab.predicted_steps(0.5) == 1
    assert lab.predicted_steps(0.0) == 0
    for k in range(1, 997):
        x = k / 997
        assert lab.predicted_steps(x) == lab.steps_to_zero(x)
