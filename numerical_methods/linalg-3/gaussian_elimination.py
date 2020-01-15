import numpy as np
from numpy.linalg import matrix_rank, solve
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from scipy.optimize import curve_fit

def test_data(nrows, ncols=None, pathological=False, whole=True, diagonal_multiplier=1, positive_definite=False):
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

def complexity(nmax, every=1, **options):
    from time import time
    from random import sample, randrange

    def n_test(n):
        t1 = time()
        gaussian_elimination(*test_data(n, **options))
        t2 = time()
        return (t2 - t1)
        
    times= []
    for n in range(2, nmax, every):
        times.append(n_test(n))
    

    model = lambda x, exponent, constant: constant * x**exponent
    popt, pcov = curve_fit(model, range(len(times)), times)
    plt.plot(times, label=f'Exponent: {popt[0]:.3f} +- {pcov[0,0]:.3f}')
    plt.plot(range(len(times)), model(range(len(times)), *popt))
    plt.legend()
    return(popt[0], pcov[0,0])