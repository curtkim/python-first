# https://ajcr.net/Basic-guide-to-einsum/
import numpy as np

def test1():
    A = np.array([0, 1, 2])
    B = np.array([ [0, 1, 2, 3], 
                    [4, 5, 6, 7],
                    [8, 9, 10, 11]])

    print( A[: ,np.newaxis]) 
    print( A.reshape(3, 1))

    print(A[:, np.newaxis] * B)
 
    np.testing.assert_equal( np.array([0, 22, 76]), np.einsum('i,ij->i', A, B))

    #assert 2 == np.searchsorted([1,2,3,4,5], 3)
    #assert 3 == np.searchsorted([1,2,3,4,5], 3, side='right')
    #np.testing.assert_equal(np.array([0, 5, 1, 2]), np.searchsorted([1,2,3,4,5], [-10, 10, 2, 3]))

def test_2d_multiply():
    A = np.array([ [1, 1, 1],
                    [2, 2, 2],
                    [5, 5, 5]])
    B = np.array([ [0, 1, 0],
                    [1, 1, 0],
                    [1, 1, 1]])
    print(np.einsum('ij,jk->ik', A, B))
