from fastcore.foundation import L


def test_L_filter():
    t = L(0, 1, 2, 3, 1, 5, 2, 7, 8, 9, 10, 11)
    assert t.filter(lambda o: o < 5) == [0, 1, 2, 3, 1, 2]


def test_L_unique():
    assert L(4, 1, 2, 3, 4, 4).unique() == [4, 1, 2, 3]

