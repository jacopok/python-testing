import numpy as np
import matplotlib.pyplot as plt
import numba
SAMPLE_SIZE = int(1e6)


@numba.njit(parallel=True)
def generate_distribution_classical(error_rate, probability_rate, gate_count):

    error_rate_1 = gate_count * error_rate
    error_rate_12 = gate_count * error_rate**2

    error_1 = np.random.random(
        size=SAMPLE_SIZE) * 2 * error_rate_1 - error_rate_1
    error_2 = np.random.random(
        size=SAMPLE_SIZE) * 2 * error_rate_1 - error_rate_1
    error_12 = np.random.random(
        size=SAMPLE_SIZE) * 2 * error_rate_12 - error_rate_12
    distribution_1 = (np.random.binomial(
        n=gate_count, p=probability_rate, size=SAMPLE_SIZE) + error_1)
    distribution_2 = (np.random.binomial(
        n=gate_count, p=probability_rate, size=SAMPLE_SIZE) + error_2)
    distribution_12 = np.maximum((np.random.binomial(
        n=gate_count, p=probability_rate**2, size=SAMPLE_SIZE) + error_12), 0)

    g = distribution_12 * gate_count / distribution_1 / distribution_2

    return g


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
def generate_distribution_quantum(error_rate, probability_rate, gate_count):

    error_rate_1 = gate_count * error_rate
    error_rate_12 = gate_count * error_rate**2

    error_1 = np.random.random(
        size=SAMPLE_SIZE) * 2 * error_rate_1 - error_rate_1
    error_2 = np.random.random(
        size=SAMPLE_SIZE) * 2 * error_rate_1 - error_rate_1
    error_12 = np.random.random(
        size=SAMPLE_SIZE) * 2 * error_rate_12 - error_rate_12
    distribution_1 = (np.random.binomial(
        n=gate_count, p=probability_rate, size=SAMPLE_SIZE) + error_1)
    distribution_2 = (np.random.binomial(
        n=gate_count, p=probability_rate, size=SAMPLE_SIZE) + error_2)
    distribution_12 = np.maximum(error_12, 0)

    g = distribution_12 * gate_count / distribution_1 / distribution_2

    return g


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
    g_q = generate_distribution_quantum(*args)
    g_c = generate_distribution_classical(*args)
    bins = np.linspace(0, 2, num=50)
    error_rate, probability_rate, gate_count = args
    plt.hist(g_q, bins=bins, density=True, alpha=.5, label='Quantum')
    plt.hist(g_c, bins=bins, density=True, alpha=.5, label='Classical')

    print(f'Quantum std: {np.std(g_q)}')
    print(f'Classical std: {np.std(g_c)}')
    plt.title(
        f'Pdfs with error {error_rate}, rate {probability_rate},'
        f' number of particles in gate {gate_count}'
    )
    plt.xlabel('$g^{(2)}$')
    plt.legend()
    plt.show(block=False)
