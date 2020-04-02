import numpy as np
import numba
from collections import namedtuple
from tqdm import tqdm

SAMPLE_SIZE_STATISTIC = int(1e4)
SAMPLE_SIZE_OUTER = int(1e2)
SAMPLE_SIZE_INNER = int(1e3)
RATES = np.logspace(-4, -1, num=int(1e1))
statistics = namedtuple('Statistics', ['average', 'std'])


@numba.njit(parallel=True)
def get_g(rate_1,
          rate_2,
          sample_size_outer=SAMPLE_SIZE_OUTER,
          sample_size_inner=SAMPLE_SIZE_INNER):
    n_1 = 0
    n_2 = 0
    n_12 = 0

    for _ in numba.prange(sample_size_outer):
        det1 = np.random.random(size=sample_size_inner)
        det2 = np.random.random(size=sample_size_inner)
        bool1 = det1 < rate_1
        bool2 = det2 < rate_2
        n_1 += np.sum(bool1)
        n_2 += np.sum(bool2)
        n_12 += np.sum(bool1 * bool2)

    if n_1 == 0 or n_2 == 0:
        return 0

    g = n_12 * (sample_size_outer * sample_size_inner) / n_1 / n_2
    return g


def get_statistics(rates_1=RATES,
                   rates_2=None,
                   number_samples=SAMPLE_SIZE_STATISTIC):

    if rates_2 is None:
        rates_2 = rates_1

    deviations = []
    means = []

    for r_1, r_2 in tqdm(zip(rates_1, rates_2)):
        gs = []
        for _ in range(number_samples):
            gs.append(get_g(r_1, r_2))
        deviations.append(np.std(gs))
        means.append(np.average(gs))

    return statistics(means, deviations)
