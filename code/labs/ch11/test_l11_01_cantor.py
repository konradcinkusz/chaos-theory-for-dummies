from labs._loader import load


def test_the_first_rounds() -> None:
    lab = load("ch11", "l11_01_cantor")
    assert lab.cantor(0) == [(0.0, 1.0)]
    one = lab.cantor(1)
    assert len(one) == 2
    assert abs(one[0][1] - 1 / 3) < 1e-12 and abs(one[1][0] - 2 / 3) < 1e-12
    two = lab.cantor(2)
    assert [round(9 * a) for a, _ in two] == [0, 2, 6, 8]


def test_pieces_double_and_the_length_shrinks() -> None:
    lab = load("ch11", "l11_01_cantor")
    assert len(lab.cantor(10)) == 2**10
    for n in range(8):
        assert abs(lab.length_left(n) - (2 / 3) ** n) < 1e-12
    assert lab.length_left(20) < 0.001


def test_a_quarter_is_never_thrown_away() -> None:
    lab = load("ch11", "l11_01_cantor")
    for n in range(12):
        assert any(a <= 0.25 <= b for a, b in lab.cantor(n))


def test_dimensions_from_copies() -> None:
    lab = load("ch11", "l11_01_cantor")
    assert abs(lab.similarity_dimension(3, 3) - 1) < 1e-12   # a line
    assert abs(lab.similarity_dimension(9, 3) - 2) < 1e-12   # a square
    assert abs(lab.similarity_dimension(4, 3) - 1.2619) < 1e-4   # Koch
    assert abs(lab.similarity_dimension(2, 3) - 0.6309) < 1e-4   # Cantor
