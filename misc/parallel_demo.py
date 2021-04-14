import numpy as np
from numba import njit, prange

@njit
def loop():

    z = np.zeros((100, 100))
    for i in range(100):
        for j in range(100):
            for k in range(100):
                z[i, j] = np.tanh(i + j) - k

    return(z)
    
@njit(parallel=True)
def parallel_loop():
    
    z = np.zeros((100, 100))
    for i in prange(100):
        for j in range(100):
            for k in range(100):
                z[i, j] = np.tanh(i + j) - k

    return(z)
