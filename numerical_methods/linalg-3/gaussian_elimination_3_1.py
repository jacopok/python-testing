import numpy as np
from numpy.linalg import matrix_rank

def gaussian_elimination(A, b):
    
    # CHECKS on the dimensionality of the problem

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

    if (matrix_rank(A) < min(n_rows, n_cols)):
        raise TypeError("Rank too low")
    
    # MAIN LOOP

    i=0
    while (i<n_rows):
        pivot = A[i, i]

        # PIVOTING
        # if the diagonal element is zero, 
        # we permute the rows of the matrix
        # and hope it is not zero anymore
        if (pivot == 0):
            for M in (A, b):
                M[i:] = np.roll(M[i:],1,axis=0)
            continue
        
        A[i,:] = A[i,:] /  pivot
        b[i] = b[i] / pivot
        for j in range(i+1, n_rows):
            # we define a variable in order for the 
            # matrix element not to change between the operations
            a = A[j,i]
            A[j,:] -= A[i,:] * a
            b[j] -= b[i] * a
        i += 1

    # BACKSUBSTITUTION
    # this works as long as the matrix is 
    # upper triangular with ones on the diagonal
    i = n_rows - 1
    x = np.zeros(n_cols)
    while (i >= 0):
        x[i] = b[i] - np.dot(A[i, i + 1:], x[i + 1:])
        i-=1

    return (x)

if __name__ == '__main__':
    
    Atest =[
       [2,  1,  4,  1],
       [3,  4, -1, -1],
       [1, -4,  1,  5],
       [2, -2,  1,  3]
       ]
    btest = [-4, 3, 9, 7]
    xtest = gaussian_elimination(Atest, btest)

    print(f'{np.array(Atest)}')
    print(f'multiplied by {xtest}')
    print(f'gives {btest}.')