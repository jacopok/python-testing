import numpy as np
import matplotlib.pyplot as plt
import numba

from simulation import g_from_detections
from simulation import detections
from simulation import simulate_detections_classical
from simulation import simulate_detections_quantum

SAMPLE_SIZE = int(1e5)


@numba.njit(parallel=True)
def box_muller(uniform, std):
    uniform_1 = uniform[::2]
    uniform_2 = uniform[1::2]
    r = np.sqrt(-2 * std**2 * np.log(1 - uniform_1))
    theta = 2 * np.pi * uniform_2
    gaussian = np.zeros_like(uniform)
    gaussian[::2] = r * np.sin(theta)
    gaussian[1::2] = r * np.cos(theta)
    return gaussian


@numba.njit(parallel=True)
def _generate_detections_classical(error_rate, rate, gate_count):
    # DOES NOT REPRODUCE CORRECT VARIANCES

    error_rate_1 = np.abs(error_rate - 2 * error_rate * rate)
    error_rate_12a = (error_rate**2 * (1 - rate)**2)
    error_rate_12b = (2 * error_rate * (1 - error_rate) * rate * (1 - rate))
    error_rate_12c = ((2 * error_rate - error_rate**2) * rate**2)
    error_rate_12 = np.abs(error_rate_12a + error_rate_12b - error_rate_12c)
    print(error_rate_12)

    error_1 = np.random.binomial(
        n=gate_count, p=error_rate_1, size=SAMPLE_SIZE) * np.sign(1 - 2 * rate)
    error_2 = np.random.binomial(
        n=gate_count, p=error_rate_1, size=SAMPLE_SIZE) * np.sign(1 - 2 * rate)
    error_12 = np.random.binomial(
        n=gate_count, p=error_rate_12,
        size=SAMPLE_SIZE) * np.sign(error_rate_12a + error_rate_12b -
                                    error_rate_12c)

    distribution_1 = (
        np.random.binomial(n=gate_count, p=rate, size=SAMPLE_SIZE) + error_1)
    distribution_2 = (
        np.random.binomial(n=gate_count, p=rate, size=SAMPLE_SIZE) + error_2)
    distribution_12 = (
        np.random.binomial(n=gate_count, p=rate**2, size=SAMPLE_SIZE) +
        error_12)

    return (distribution_1, distribution_2, distribution_12, gate_count)


def generate_detections_classical(*args):
    return (detections(*_generate_detections_classical(*args)))


def generate_distribution_classical(*args):
    return (g_from_detections(*generate_detections_classical(*args)))


def plot_distribution_classical(*args):
    g = generate_distribution_classical(*args)
    plt.hist(g,
             bins=200,
             density=True,
             alpha=.5,
             label=', '.join([f'{x}' for x in args]))

    error_rate, probability_rate, gate_count = args
    print(f'Error rate: {error_rate}')
    print(f'Probability rate: {probability_rate}')
    print(f'Gate count: {gate_count}')
    print(f'Standard deviation: {np.std(g)}')
    plt.legend()
    # plt.show(block=False)


@numba.njit(parallel=True)
def _generate_detections_quantum(error_rate, probability_rate, gate_count):

    error_rate_1 = gate_count * error_rate
    error_rate_12 = gate_count * error_rate**2

    error_1 = box_muller(np.random.random(size=SAMPLE_SIZE), error_rate_1)
    error_2 = box_muller(np.random.random(size=SAMPLE_SIZE), error_rate_1)
    error_12 = box_muller(np.random.random(size=SAMPLE_SIZE), error_rate_12)
    distribution_1 = (np.random.binomial(
        n=gate_count, p=probability_rate, size=SAMPLE_SIZE) + error_1)
    distribution_2 = (np.random.binomial(
        n=gate_count, p=probability_rate, size=SAMPLE_SIZE) + error_2)
    distribution_12 = np.maximum(error_12, 0)

    return (distribution_1, distribution_2, distribution_12, gate_count)


def generate_detections_quantum(*args):
    return (detections(*_generate_detections_quantum(*args)))


def generate_distribution_quantum(*args):
    return (g_from_detections(*generate_detections_quantum(*args)))


def plot_distribution_quantum(*args):
    g = generate_distribution_quantum(*args)
    plt.hist(g,
             bins=200,
             density=True,
             alpha=.5,
             label=', '.join([f'{x}' for x in args]))

    error_rate, probability_rate, gate_count = args
    print(f'Error rate: {error_rate}')
    print(f'Probability rate: {probability_rate}')
    print(f'Gate count: {gate_count}')
    print(f'Standard deviation: {np.std(g)}')
    plt.legend()
    # plt.show(block=False)


def plot_both_distributions(*args):
    g_q = g_from_detections(*simulate_detections_quantum(*args))
    g_c = g_from_detections(*simulate_detections_classical(*args))
    bins = np.linspace(0, 2, num=200)
    sample_size, probability_rate, error_rate = args
    plt.hist(g_q, bins=bins, density=True, alpha=.5, label='Quantum')
    plt.hist(g_c, bins=bins, density=True, alpha=.5, label='Classical')

    print(f'Quantum std: {np.std(g_q)}')
    print(f'Classical std: {np.std(g_c)}')
    plt.title(f'Pdfs with error {error_rate:.4f}, rate {probability_rate:.4f}'
              f', sample size {sample_size}')
    plt.xlabel('$g^{(2)}$')
    plt.legend()
    plt.show(block=False)


def check_simulation(e_rate, rate, N_gate):
    x = simulate_detections(SAMPLE_SIZE, rate, rate, e_rate, e_rate,
                            int(np.sqrt(N_gate)), int(np.sqrt(N_gate)))
    y = generate_detections_classical(e_rate, rate, N_gate)
    plt.hist(x.N_12, label='sim', alpha=.5, density=True)
    plt.hist(y.N_12, label='gen', alpha=.5, density=True)
    plt.legend()
    plt.show()