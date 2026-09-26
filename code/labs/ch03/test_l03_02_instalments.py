from labs._loader import load


def test_one_instalment_is_the_chapters_rule() -> None:
    lab = load("ch03", "l03_02_instalments")
    assert abs(lab.next_gen(0.3, 2.0) - 0.42) < 1e-12
    for x in (0.01, 0.2, 0.5, 0.9):
        once = lab.in_instalments(x, 2.8, 1)
        assert abs(once - lab.next_gen(x, 2.8)) < 1e-15


def test_instalments_add_up_in_order() -> None:
    lab = load("ch03", "l03_02_instalments")
    # two instalments of half a change each, worked out one after another
    first = 0.2 + (2.8 * 0.2 * 0.8 - 0.2) / 2
    second = first + (2.8 * first * (1 - first) - first) / 2
    assert abs(lab.in_instalments(0.2, 2.8, 2) - second) < 1e-12


def test_both_settle_at_the_same_level() -> None:
    lab = load("ch03", "l03_02_instalments")
    once = lab.run(2.8, 1, 0.01, 200)
    paid = lab.run(2.8, 10, 0.01, 200)
    assert len(once) == len(paid) == 201
    assert once[0] == paid[0] == 0.01
    assert abs(once[-1] - (1 - 1 / 2.8)) < 1e-6
    assert abs(paid[-1] - (1 - 1 / 2.8)) < 1e-9


def test_only_the_late_one_overshoots() -> None:
    lab = load("ch03", "l03_02_instalments")
    assert lab.overshoots(2.8, 1)
    assert not lab.overshoots(2.8, 10)
    assert not lab.overshoots(1.5, 1)
