import numpy as np
from numpy.random import rand

def test_data(nrows, ncols=None, pathological=False, whole=True, diagonal_multiplier=1, positive_definite=False):
    if (not ncols):
        ncols = nrows
    if(whole):
        A = np.array(rand(nrows, ncols)*10, dtype=int)
        b = np.array(rand(nrows)*10, dtype=int)
    else:
        A = rand(nrows,ncols)
        b = rand(nrows)
    if(pathological):
        for i in range(min(nrows,ncols)):
            A[i, i] = 0
    else:
        for i in range(min(nrows,ncols)):
            if (A[i, i] == 0):
                A[i, i] += 1
    for i in range(min(nrows, ncols)):
        A[i, i] *= diagonal_multiplier
    if (positive_definite):
        A = A @ A.T
    return(A, b)