import numpy as np
from numpy.linalg import det, solve
from time import sleep

def test_data(n, pathological=False):
    from numpy.random import rand
    A = np.array(rand(n, n)*10, dtype=int)
    b = np.array(rand(n)*10, dtype=int)
    # b = rand(n)
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
    A = np.array(A, dtype=np.float64)
    b = np.array(b, dtype=np.float64)

    scale = np.average([np.average(np.abs(A.flatten())), np.average(np.abs(b))])

    def is_zero(x, scale=scale, threshold=1e-10):
        """
        Check whether a number is significantly 
        less than "scale", the average absolute value of the numbers in the tensors at hand. 
        This is done instead of a constant threshold to prevent issues with matrices of very small or large numbers.
        """

        return(np.abs(x)<threshold*scale)

    if (is_zero(det(A))):
        raise TypeError("Zero determinant")
        
    print("Solutions", solve(A, b))
    print(A, b)
    
    i=0
    while (i<n_cols):
        pivot = A[i, i]
        if (pivot == 0):
            # print("Rolling", A, b)
            for x in (A, b):
                x[i:] = np.roll(x[i:],1,axis=0)
            # A[i:,:] = np.roll(A[i:], 1, axis=0)
            # b[i:] = np.roll(b[i:], 1, axis=0)
            # print("Result", A, b)
            continue
        A[i,:] = A[i,:] /  pivot
        b[i] = b[i] / pivot
        for j in range(i+1, n_rows):
            A[j,:] -= A[i,:] * A[j, i]
            b[j] -= b[i] * A[j, i]
        i += 1
    
    print("My solutions", solve(A, b))

    return(A, b)