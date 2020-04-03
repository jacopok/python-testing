import numpy as np
import numba
from collections import namedtuple
from tqdm import tqdm

SAMPLE_SIZE_STATISTIC = int(1e4)
SAMPLE_SIZE_OUTER = int(1e2)
SAMPLE_SIZE_INNER = int(1e3)
RATES = np.logspace(-4, -1, num=int(1e1))
statistics = namedtuple('Statistics', ['average', 'std'])
detections = namedtuple('Detections', ['N_1', 'N_2', 'N_12', 'N_gate'])


@numba.njit(parallel=True)
def _simulate_detection_classical(rate_1,
                                  e_rate_1=0,
                                  rate_2=0,
                                  e_rate_2=0,
                                  sample_size_outer=SAMPLE_SIZE_OUTER,
                                  sample_size_inner=SAMPLE_SIZE_INNER):

    if not (rate_2):
        rate_2 = rate_1

    if not (e_rate_2):
        e_rate_2 = e_rate_1

    n_1 = 0
    n_2 = 0
    n_12 = 0

    for _ in numba.prange(sample_size_outer):
        det1 = np.random.random(size=sample_size_inner)
        det2 = np.random.random(size=sample_size_inner)
        err1 = np.random.random(size=sample_size_inner)
        err2 = np.random.random(size=sample_size_inner)

        bool1 = det1 < rate_1 / 2
        bool2 = det2 < rate_2 / 2

        e_bool1 = err1 < e_rate_1
        e_bool2 = err2 < e_rate_2

        bool1 = np.logical_or(bool1, e_bool1)
        bool2 = np.logical_or(bool2, e_bool2)

        n_1 += np.sum(bool1)
        n_2 += np.sum(bool2)
        n_12 += np.sum(bool1 * bool2)

    return (n_1, n_2, n_12, sample_size_inner * sample_size_outer)


@numba.njit(parallel=True)
def _simulate_detection_quantum(rate_1,
                                e_rate_1=0,
                                rate_2=0,
                                e_rate_2=0,
                                sample_size_outer=SAMPLE_SIZE_OUTER,
                                sample_size_inner=SAMPLE_SIZE_INNER):

    if not (rate_2):
        rate_2 = rate_1

    if not (e_rate_2):
        e_rate_2 = e_rate_1

    n_1 = 0
    n_2 = 0
    n_12 = 0

    for _ in numba.prange(sample_size_outer):
        which_way = np.random.random(size=sample_size_inner) > .5

        det1 = np.random.random(size=sample_size_inner)
        det2 = np.random.random(size=sample_size_inner)
        err1 = np.random.random(size=sample_size_inner)
        err2 = np.random.random(size=sample_size_inner)

        bool1 = np.logical_and(det1 < rate_1, which_way)
        bool2 = np.logical_and(det2 < rate_2, np.logical_not(which_way))

        e_bool1 = err1 < e_rate_1
        e_bool2 = err2 < e_rate_2

        bool1 = np.logical_or(bool1, e_bool1)
        bool2 = np.logical_or(bool2, e_bool2)

        n_1 += np.sum(bool1)
        n_2 += np.sum(bool2)
        n_12 += np.sum(bool1 * bool2)

    return (n_1, n_2, n_12, sample_size_inner * sample_size_outer)


def simulate_detection_classical(*args):
    return detections(*_simulate_detection_classical(*args))


def simulate_detection_quantum(*args):
    return detections(*_simulate_detection_quantum(*args))


def simulate_detections_classical(size, *args):
    n_1_arr = []
    n_2_arr = []
    n_12_arr = []
    n_gate_arr = []

    for _ in range(size):
        det = simulate_detection_classical(*args)
        n_1, n_2, n_12, n_gate = det
        n_1_arr.append(n_1)
        n_2_arr.append(n_2)
        n_12_arr.append(n_12)
        n_gate_arr.append(n_gate)

    return (detections(np.array(n_1_arr), np.array(n_2_arr),
                       np.array(n_12_arr), np.array(n_gate_arr)))


def simulate_detections_quantum(size, *args):
    n_1_arr = []
    n_2_arr = []
    n_12_arr = []
    n_gate_arr = []

    for _ in range(size):
        det = simulate_detection_quantum(*args)
        n_1, n_2, n_12, n_gate = det
        n_1_arr.append(n_1)
        n_2_arr.append(n_2)
        n_12_arr.append(n_12)
        n_gate_arr.append(n_gate)

    return (detections(np.array(n_1_arr), np.array(n_2_arr),
                       np.array(n_12_arr), np.array(n_gate_arr)))


def g_from_detections(*detections):
    n_1, n_2, n_12, n_gate = detections

    return n_12 * n_gate / n_1 / n_2


def simulate_g(*args):
    n_1, n_2, n_12, n_gate = simulate_detection_classical(*args)

    g = g_from_detections(n_1, n_2, n_12, n_gate)
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
            gs.append(g_from_detections(r_1, r_2))
        deviations.append(np.std(gs))
        means.append(np.average(gs))

    return statistics(means, deviations)
