import numpy as np
from numpy.linalg import matrix_rank

def gauss_seidel(A, b, ansatz=None, relaxation=1):
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

    def iteration_step(A, b, x, relaxation):
        xnew = np.zeros(np.shape(x))
        for i in range(len(x)):
            xnew[i] = 1 / A[i, i] * (b[i] - A[i,:] * x + A[i, i] * x[i])
        return (relaxation*xnew - (1-relaxation) * x)
    
    