import numpy as np
from numpy.linalg import matrix_rank, solve

def test_data(nrows, ncols=None, pathological=False, whole=True):
    from numpy.random import rand
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

    if (matrix_rank(A) < min(n_rows, n_cols)):
        raise TypeError("Rank too low")
        
    i=0
    while (i<n_rows):
        pivot = A[i, i]
        if (pivot == 0):
            for x in (A, b):
                x[i:] = np.roll(x[i:],1,axis=0)
            continue
        A[i,:] = A[i,:] /  pivot
        b[i] = b[i] / pivot
        for j in range(i+1, n_rows):
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

def LU_decomposition(A):

    A_shape = np.shape(A)
    if (len(A_shape) != 2):
        raise TypeError("A must be a 2D matrix")

    n_rows, n_cols = A_shape
    A = np.array(A, dtype=np.float64)
    Linv = np.eye(n_rows)

    if (matrix_rank(A) < min(n_rows, n_cols)):
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
    
    return(A, Linv)

def complexity(nmax, every=1, *options):
    from time import time
    from random import sample, randrange

    def n_test(n):
        t1 = time()
        gaussian_elimination(*test_data(n, *options))
        t2 = time()
        return (t2 - t1)
        
    times= []
    for n in range(1, nmax, every):
        times.append(n_test(n))
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    model = lambda x, exponent, constant: constant * x**exponent
    plt.style.use('seaborn')
    popt, pcov = curve_fit(model, range(len(times)), times)
    plt.plot(times, label=f'Exponent: {popt[0]:.3f} +- {pcov[0,0]:.3f}')
    plt.plot(range(len(times)), model(range(len(times)), *popt))
    plt.legend()
    return(popt[0], pcov[0,0])