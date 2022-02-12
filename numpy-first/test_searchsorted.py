import numpy as np

def test1():
    assert 2 == np.searchsorted([1,2,3,4,5], 3)
    assert 3 == np.searchsorted([1,2,3,4,5], 3, side='right')
    np.testing.assert_equal(np.array([0, 5, 1, 2]), np.searchsorted([1,2,3,4,5], [-10, 10, 2, 3]))

