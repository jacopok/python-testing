import numpy as np
from numpy.linalg import det, solve
from time import sleep

def test_data(n, pathological=False):
    from numpy.random import rand
    A = rand(n, n)
    b = rand(n)
    if(pathological):
        for i in range(n):
            A[i,i] = 0
    return(A, b)

def gaussian_elimination(A, b):
    A_shape = np.shape(A)
    b_shape = np.shape(b)
    if (len(A_shape) != 2):
        raise TypeError("A must be a 2D matrix")
    if (len(b_shape) != 1):
        raise TypeError("b must be a 1D vector")
    if (A_shape[0] != b_shape[0]):
        raise TypeError("column number of A must equal dimension of b")

    n_rows, n_cols = A_shape
    A = np.array(A)
    b = np.array(b)
    # print(solve(A, b))

    scale = np.average([np.average(np.abs(A.flatten())), np.average(np.abs(b))])

    def is_zero(x, scale=scale, threshold=1e-10):
        return(np.abs(x)<threshold*scale)

    if (is_zero(det(A))):
        raise TypeError("Zero determinant")
    
    def roll(A, start=0):
        for j in range(start, len(A) - 1):
            A[j], A[j + 1] = A[j + 1], A[j]
        return (A)
    
    print("Solutions", solve(A, b))
    
    i=0
    while (i<n_cols):
        pivot = A[i, i]
        # print("Det:", det(A))
        # print(A)
        if (pivot == 0):
            A[i:,:] = np.roll(A[i:,:], 1, axis=0)
            b[i:] = np.roll(b[i:], 1, axis=0)
            # A = roll(A)
            sleep(1)
            continue
        A[i,:] /= pivot
        for j in range(i+1, n_rows):
            A[j,:] -= A[i,:] * A[j, i]
            b[j] -= b[i] * A[j, i]
        i += 1
    
    print("My solutions", solve(A, b))

    return(A, b)