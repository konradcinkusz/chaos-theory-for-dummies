from labs._loader import load

# The superstable landmarks of Chapter 8, periods 1, 2, 4, ..., 256.
LOGISTIC = [2.0, 3.2360679775, 3.4985616993, 3.5546408628, 3.5666673799,
            3.5692435316, 3.5697952937, 3.5699134654, 3.5699387742]
SINE = [0.5, 0.777733766172, 0.846382171707, 0.861450350883,
        0.864694180746, 0.865389673405, 0.865538661605, 0.865570571920,
        0.865577406206]


def test_ratios_of_a_sequence_that_halves() -> None:
    lab = load("ch08", "l08_02_ratio")
    assert lab.ratios([0.0, 1.0, 1.5, 1.75]) == [2.0, 2.0]
    assert lab.where_it_ends([0.0, 1.0, 1.5, 1.75]) == 2.0


def test_the_logistic_ratio_settles_on_feigenbaums_number() -> None:
    lab = load("ch08", "l08_02_ratio")
    rs = lab.ratios(LOGISTIC)
    assert len(rs) == len(LOGISTIC) - 2
    assert abs(rs[0] - 4.7089) < 1e-4
    assert abs(rs[-1] - 4.66919) < 1e-4
    assert abs(lab.where_it_ends(LOGISTIC) - 3.5699457) < 1e-6


def test_the_sine_map_gives_the_same_ratio_somewhere_else() -> None:
    lab = load("ch08", "l08_02_ratio")
    rs = lab.ratios(SINE)
    assert abs(rs[0] - 4.0457) < 1e-3
    assert abs(rs[-1] - 4.66915) < 1e-4
    assert abs(lab.where_it_ends(SINE) - 0.8655793) < 1e-6
