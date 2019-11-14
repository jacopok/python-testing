import numpy as np
from numpy.linalg import matrix_rank

def gauss_seidel(A, b, ansatz=None, eps = 1e-5):
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
    
    def dist(x1, x2):
        return (np.sum(np.abs(x1 - x2)))
    
    def norm(x):
        return (np.sum(np.abs(x)))
    
    if (ansatz):
        xnew = ansatz
    else:
        xnew = b

    # iteration number
    n = 0
    for _ in range(10):
        xold, xnew = xnew, iteration_step(A, b, xnew, 1)
        n+=1
    
    Dxk = dist(xold,xnew)

    Oopt=[]
    for p in range(1,10):
        xold, xnew = xnew, iteration_step(A, b, xnew, 1)
        Dx= dist(xnew, xold)
        Oopt.append(2/(1+np.sqrt(1-(Dx/Dxk)**(1/p))))
        n += 1
    
    Oopt = np.average(Oopt)

    while dist(xold, xnew) < eps * norm(xnew):
        xold, xnew = xnew, iteration_step(A, b, xnew, Oopt)
        n += 1

    return(xnew)