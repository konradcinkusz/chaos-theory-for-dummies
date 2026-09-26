from labs._loader import load


def test_knead_stretches_then_folds() -> None:
    lab = load("ch10", "l10_01_knead")
    assert lab.knead(0.25) == 0.5          # stretched, nothing to fold
    assert lab.knead(0.75) == 0.5          # stretched to 1.5, folded back
    assert lab.knead(0.5) == 1.0
    assert abs(lab.knead(0.9) - 0.2) < 1e-12


def test_the_dough_never_leaves_the_board() -> None:
    lab = load("ch10", "l10_01_knead")
    x = 0.2345
    for _ in range(40):
        x = lab.knead(x)
        assert 0.0 <= x <= 1.0


def test_close_raisins_part_after_a_few_kneads() -> None:
    lab = load("ch10", "l10_01_knead")
    # a thousandth apart; 0.001 * 2**7 = 0.128 is the first gap over 0.1
    assert lab.kneads_until_apart(0.2345, 0.001, 0.1) == 7
    # ten times closer buys only three more kneads: 2 * 2 * 2 is about 10
    assert lab.kneads_until_apart(0.2345, 0.0001, 0.1) == 10
