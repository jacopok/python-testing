import numpy as np
import numba

SAMPLE_SIZE_STATISTIC = int(1e4)
SAMPLE_SIZE_OUTER = int(1e2)
SAMPLE_SIZE_INNER = int(1e3)
RATES = np.linspace(.1, 1, num=int(1e1))

@numba.njit(parallel=True)
def get_g(rate, sample_size_outer=SAMPLE_SIZE_OUTER, sample_size_inner=SAMPLE_SIZE_INNER):
    n_1 = 0
    n_2 = 0
    n_12 = 0

    for _ in numba.prange(sample_size_outer):
        det1 = np.random.random(size=sample_size_inner)
        det2 = np.random.random(size=sample_size_inner)
        bool1 = det1 < rate
        bool2 = det2 < rate
        n_1 += np.sum(bool1)
        n_2 += np.sum(bool2)
        n_12 += np.sum(bool1*bool2)

    g = n_12 * (sample_size_outer*sample_size_inner) / n_1 / n_2
    return g

def get_statistics(rates=RATES, number_samples=SAMPLE_SIZE_STATISTIC):

    deviations = []
    means = []

    for r in rates:
        gs=[]
        for _ in range(number_samples):
            gs.append(get_g(r))
        deviations.append(np.std(gs))
        means.append(np.average(gs))
    
    return (means, deviations)
    
