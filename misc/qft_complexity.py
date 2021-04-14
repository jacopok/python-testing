import numpy as np
from tqdm import tqdm
from functools import lru_cache
from numba import njit, prange
    
ms = np.ones(2 * L)  # all masses set to one, easily customizable
THETA = 2
OMEGA_0 = L 

SQRT_PLUS = np.sqrt(1 + np.tanh(THETA))
SQRT_MINUS = np.sqrt(1 - np.tanh(THETA))
PI_OVER_TWO_L = np.pi / 2 / L

# @lru_cache(maxsize=4 * L ** 2)
@njit
def phi_hom(n, i, j):
    # zero-indexed! 
    return (np.cos((i + .5) * n * PI_OVER_TWO_L)
            * np.cos((j + .5) * n * PI_OVER_TWO_L) / L)
    
# @lru_cache(maxsize=4 * L ** 2)
@njit
def D(i, j):
    sign = (i // L + j % 2) % 2
    # 0 maps to +, 1 maps to -
    
    if sign == 0:
        return SQRT_PLUS
    return SQRT_MINUS

# @lru_cache(maxsize=2 * L)
@njit
def omega(m):
    # zero-indexed! 
    cosine_term = 2 * (1 - np.cos(m * PI_OVER_TWO_L))
    return np.sqrt(OMEGA_0 ** 2 + cosine_term)
    
@njit(parallel=True)
def qq(L):
    
    qq_matrix = np.zeros((2 * L, 2 * L))
    
    # for (i, j), _ in tqdm(np.ndenumerate(qq_matrix), total=4 * L**2):
    # for (i, j), _ in np.ndenumerate(qq_matrix):
    for i in prange(2 * L):
        for j in range(2 * L):
            for n in range(2 * L):
                qq_matrix[i, j] += D(i, n) * D(j, n) * phi_hom(n, i, j) / omega(n)
            qq_matrix[i, j] *= np.sqrt(ms[i] * ms[j]) / 2.
    
    return qq_matrix