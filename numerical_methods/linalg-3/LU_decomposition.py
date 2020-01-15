import numpy as np
from gaussian_elimination_3_1 import gaussian_elimination

def LU_decomposition(A):
    """
    Given a matrix A, returns (U, Linv), such that:
    A = L@U
    and L^-1 = Linv
    """

    A_shape = np.shape(A)
    if (len(A_shape) != 2):
        raise TypeError("A must be a 2D matrix")

    n_rows, n_cols = A_shape
    A = np.array(A, dtype=np.float64)
    Linv = np.eye(n_rows)

    if (np.linalg.matrix_rank(A) < min(n_rows, n_cols)):
        raise TypeError("Rank too low")
        
    i=0
    while (i<n_rows):
        pivot = A[i, i]
        if (pivot == 0):
            for x in (A, Linv):
                x[i:] = np.roll(x[i:],1,axis=0)
            continue
        A[i,:] = A[i,:] /  pivot
        Linv[i,:] = Linv[i,:] / pivot
        for j in range(i+1, n_rows):
            a = A[j,i]
            A[j,:] -= A[i,:] * a
            Linv[j,:] -= Linv[i,:] * a
        i += 1
    
    return (A, Linv)
    
if __name__ == '__main__':
    Atest = np.array([
       [2,  1,  4,  1],
       [3,  4, -1, -1],
       [1, -4,  1,  5],
       [2, -2,  1,  3]
       ])
    btest = np.array([-4, 3, 9, 7])

    # If A = L@U, 
    # then U@x = Linv@b
    # has the same solutions as
    # A@x = b
    
    U, Linv = LU_decomposition(Atest)
    print(gaussian_elimination(U, Linv @ btest))
    print(gaussian_elimination(Atest, btest))