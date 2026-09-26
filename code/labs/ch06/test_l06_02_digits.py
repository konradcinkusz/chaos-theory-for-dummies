from labs._loader import load


def test_a_worked_pair() -> None:
    lab = load("ch06", "l06_02_digits")
    # 0.625 is 0.101 in binary and 0.75 is 0.110: they share one digit
    assert lab.shared_digits(0.625, 0.75) == 1
    assert lab.steps_together(0.625, 0.75) == 1


def test_the_twins_of_the_chapter() -> None:
    lab = load("ch06", "l06_02_digits")
    a, b = 0.2, 0.2 + 1e-10
    assert lab.shared_digits(a, b) == 32
    assert lab.steps_together(a, b) == 32


def test_digits_and_steps_always_agree() -> None:
    lab = load("ch06", "l06_02_digits")
    for i in range(1, 200):
        a = i / 201
        b = a + 2.0 ** -(i % 40 + 1)
        if b >= 1.0:
            continue
        assert lab.shared_digits(a, b) == lab.steps_together(a, b)


def test_equal_numbers_stop_at_the_limit() -> None:
    lab = load("ch06", "l06_02_digits")
    assert lab.shared_digits(0.3, 0.3, limit=40) == 40
    assert lab.steps_together(0.3, 0.3, limit=40) == 40
