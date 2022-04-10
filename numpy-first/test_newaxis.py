import numpy as np


def test_newaxis_row_column_vector():
    arr = np.arange(4)
    assert (4,) == arr.shape

    row_vec = arr[np.newaxis, :]
    assert (1, 4) == row_vec.shape

    col_vec = arr[:, np.newaxis]
    assert (4, 1) == col_vec.shape


def test_add_dimension():
    arr = np.arange(5*5).reshape(5, 5)
    arr_5D = arr[np.newaxis, ..., np.newaxis, np.newaxis]
    assert (1, 5, 5, 1, 1) == arr_5D.shape

