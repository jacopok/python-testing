import numpy as np

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
    for i in range(n_rows):
        # print(A)
        for j in range(i):
            b[i] -= A[i, j] * b[j]
            A[i,:] -= A[i, j] * A[j,:]
        if (A[i, i] == 0):
            # print("Swapping")
            # print(A)
            A[i,:], A[-1,:] = A[-1,:], A[i,:]
            b[i], b[-1] = b[-1], b[i]
            # print(A)
            pass 
        b[i] = b[i] / A[i, i]
        A[i,:] = A[i,:] / A[i, i]
    
    return(A, b)