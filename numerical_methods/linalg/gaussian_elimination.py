import numpy as np

def test_data(n):
    nums = range(n ** 2)
    from random import sample
    nums = sample(nums, k=n ** 2)
    nums_vec = range(n)
    nums_vec = sample(nums_vec, k = n)
    return(np.reshape(nums, (n,n)), nums_vec)

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
    print("Starting b")
    print(b)
    for i in range(n_rows):
        if(A[i, i] != 0):
            A[i,:] = A[i,:] / A[i, i]
            b[i] = b[i] / A[i, i]
        for j in range(i):
            A[i,:] -= A[i, j] * A[j,:]
            b[i] -= A[i, j] * b[j]
    
    print("Ending b")
    print(b)
    return(A, b)