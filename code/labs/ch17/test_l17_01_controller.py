from labs._loader import load

R0 = 3.9
TARGET = 1.0 - 1.0 / R0


def test_no_nudge_when_far_away() -> None:
    lab = load("ch17", "l17_01_controller")
    assert lab.nudge(0.2, R0, 0.039) == 0.0
    assert lab.nudge(TARGET + 0.01, R0, 0.039) == 0.0


def test_a_nudge_cancels_the_miss() -> None:
    lab = load("ch17", "l17_01_controller")
    x = TARGET + 0.001
    change = lab.nudge(x, R0, 0.039)
    assert abs(change - 0.009965) < 1e-5      # about ten times the miss
    after = (R0 + change) * x * (1.0 - x)
    # left alone the miss would become 0.0019; nudged, it nearly vanishes
    assert abs(after - TARGET) < 1e-4


def test_the_orbit_is_caught_and_held() -> None:
    lab = load("ch17", "l17_01_controller")
    xs, changes = lab.hold(0.2, R0, 400, 0.039)
    assert len(xs) == 401 and len(changes) == 400
    assert max(abs(c) for c in changes) <= 0.039
    assert all(abs(x - TARGET) < 1e-12 for x in xs[300:])


def test_it_works_at_another_r() -> None:
    lab = load("ch17", "l17_01_controller")
    r0 = 3.7
    xs, changes = lab.hold(0.3, r0, 3000, 0.01 * r0)
    assert max(abs(c) for c in changes) <= 0.01 * r0
    assert abs(xs[-1] - (1.0 - 1.0 / r0)) < 1e-12
