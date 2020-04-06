import numpy as np
import matplotlib.pyplot as plt
import numba

from simulation import g_from_detections
from simulation import detections
from simulation import simulate_detections_classical
from simulation import simulate_detections_quantum
from scipy.stats import gaussian_kde
import astropy.units as u
from tqdm import tqdm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cm import coolwarm

from scipy.integrate import trapz
from scipy.stats import norm

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
    bins = np.logspace(-5, .5, num=1000)
    bins[0] = 0
    sample_size, probability_rate, error_rate, *_ = args

    # plt.semilogy(bins, gaussian_kde(g_q).pdf(bins), label='Quantum')
    # plt.semilogy(bins, gaussian_kde(g_c).pdf(bins), label='Classical')
    # plt.plot(bins, gaussian_kde(g_q).pdf(bins) / gaussian_kde(g_c).pdf(bins), label='Ratio')

    plt.hist(g_q, bins=bins, density=True, alpha=.5, label='Quantum')
    plt.hist(g_c, bins=bins, density=True, alpha=.5, label='Classical')
    plt.xscale('symlog', linthreshx=1e-5)
    plt.yscale('symlog')

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


def get_bayes_factor(g_measurement, sample_size, rate, e_rate, N_gate):
    g_distribution_classical = g_from_detections(
        *simulate_detections_classical(sample_size, rate, e_rate, rate, e_rate,
                                       int(np.sqrt(N_gate)),
                                       int(np.sqrt(N_gate))))
    g_distribution_quantum = g_from_detections(*simulate_detections_quantum(
        sample_size, rate, e_rate, rate, e_rate, int(np.sqrt(N_gate)),
        int(np.sqrt(N_gate))))

    classical_logpdf = gaussian_kde(g_distribution_classical).logpdf(
        g_measurement)

    try:
        quantum_logpdf = gaussian_kde(g_distribution_quantum).logpdf(
            g_measurement)
    except np.linalg.LinAlgError:
        quantum_logpdf = 0.

    bayes_ratio_nepers = quantum_logpdf - classical_logpdf

    bayes_ratio = bayes_ratio_nepers / np.log(10) * u.dex(1)

    return bayes_ratio


def get_bayes_factor_parametric(g_measurement, sample_size, rate, e_rate,
                                parameters_prior, N_gate):
    """the shape if parameters_prior should be (len(rate), len(e_rate))

    Should be called like:
    i, p, r, prior = get_bayes_factor_parametric(g, 200, rate, e_rate, param_prior, N_G.n)
    
    after running the file 
    `parameter_estimates.py`
    
    then plot like 
    `plot_logpdf(*r, p[i])`
    
    where i = 0, 1
    """

    to_sim = sample_size * parameters_prior.size * N_gate

    print(f'Need to compute {sample_size=} times '
          f'{parameters_prior.size=} times {N_gate=}')
    print(f'detections, which means 10 to the {np.log10(to_sim):.1f}')

    data_given_model_classical = np.zeros_like(parameters_prior)
    print('Estimating classical data-given-model')

    for i, r in enumerate(rate):
        print(f'{i+1} out of {len(rate)}')
        for j, e in tqdm(enumerate(e_rate)):
            g_distribution_classical = g_from_detections(
                *simulate_detections_classical(sample_size, r, e, r, e,
                                               int(np.sqrt(N_gate)),
                                               int(np.sqrt(N_gate))))
            try:
                data_given_model_classical[i, j] = gaussian_kde(
                    g_distribution_classical).pdf(g_measurement)
            except (np.linalg.LinAlgError, ValueError):
                if np.isclose(g_measurement, g_distribution_classical).all():
                    data_given_model_classical[i, j] = 1
                else:
                    data_given_model_classical[i, j] = 0

    data_given_model_quantum = np.zeros_like(parameters_prior)
    print('Estimating quantum data-given-model')

    for i, r in enumerate(rate):
        print(f'{i+1} out of {len(rate)}')
        for j, e in tqdm(enumerate(e_rate)):
            g_distribution_quantum = g_from_detections(
                *simulate_detections_quantum(sample_size, r, e, r, e,
                                             int(np.sqrt(N_gate)),
                                             int(np.sqrt(N_gate))))
            try:
                data_given_model_quantum[i, j] = gaussian_kde(
                    g_distribution_quantum).pdf(g_measurement)
            except (np.linalg.LinAlgError, ValueError):
                if np.isclose(g_measurement, g_distribution_quantum).all():
                    data_given_model_quantum[i, j] = 1
                else:
                    data_given_model_quantum[i, j] = 0

    print('Integrating')
    rate_len, e_rate_len = np.shape(parameters_prior)
    integrand_classical = parameters_prior * data_given_model_classical
    integrand_quantum = parameters_prior * data_given_model_quantum

    if rate_len > 1:
        integrand_classical = trapz(y=integrand_classical, x=rate, axis=0)
        integrand_quantum = trapz(y=integrand_quantum, x=rate, axis=0)
    else:
        integrand_classical = integrand_classical[0]
        integrand_quantum = integrand_quantum[0]

    if e_rate_len > 1:
        # axis 0 is now what was axis 1 before
        likelihood_classical = trapz(y=integrand_classical, x=e_rate, axis=0)
        likelihood_quantum = trapz(y=integrand_quantum, x=e_rate, axis=0)
    else:
        likelihood_classical = integrand_classical[0]
        likelihood_quantum = integrand_quantum[0]

    from datetime import datetime
    now = datetime.now().isoformat()
    path = 'simulations/'
    to_save = {
        'dgm_classical': data_given_model_classical,
        'dgm_quantum': data_given_model_quantum,
        'rate': rate,
        'e_rate': e_rate,
        'param_prior': parameters_prior
    }

    with open(path + 'result_' + now + '.txt', 'w') as f:
        f.writelines('\n'.join([
            f'Classical pdf value: {likelihood_classical}',
            f'Quantum pdf value: {likelihood_quantum}',
            f'Ratio (log10): {-np.log10(likelihood_classical/likelihood_quantum)}',
            f'N_gate: {N_gate}', f'sample size: {sample_size}',
            f'parameter pdf shape: {parameters_prior.shape}',
            f'g_measurement: {g_measurement}'
        ]))

    for name, x in to_save.items():
        np.save(path + name + '_' + now, x)

    return ((likelihood_classical, likelihood_quantum),
            (data_given_model_classical,
             data_given_model_quantum), (rate, e_rate), parameters_prior)


def lognormal_dist(mean, std, num=40):
    def dist(x):
        n = 1 / x / std / np.sqrt(2 * np.pi)
        a = -(np.log(x) - mean)**2 / 2 / std**2
        return (n * np.exp(a))

    param = np.logspace(mean - 3 * std,
                        min(mean + 3 * std, 0),
                        base=np.e,
                        num=num)

    return (param, dist(param))


def loguniform_dist(lower_log, upper_log, num=40):

    param = np.logspace(lower_log, min(upper_log, 0), base=np.e, num=num)

    dist = np.ones_like(param)
    normalization = trapz(y=dist, x=param)
    # = 1, but just to be sure

    return (param, dist / normalization)


def uniform_dist(lower_log, upper_log, num=40):

    param = np.logspace(lower_log, min(upper_log, 0), base=np.e, num=num)

    dist = np.copy(param)
    normalization = trapz(y=dist, x=param)

    return (param, dist / normalization)


def normal_dist(mean, std, num=40):

    param = np.logspace(np.log(mean - 3 * std),
                        min(np.log(mean + 3 * std), 0),
                        base=np.e,
                        num=num)

    dist = norm(loc=mean, scale=std).pdf(param)

    return (param, dist)


def plot_logpdf(rate, e_rate, pdf):

    fig = plt.figure()
    # ax = fig.gca(projection='3d')
    ax = fig.gca()
    
    cmap = plt.get_cmap('viridis')
    
    ax.set_facecolor(cmap.colors[0])
    # X, Y = np.meshgrid(np.log(rate), np.log(e_rate), indexing='ij')

    log_xy = np.log(np.outer(rate, e_rate))

    # ax.plot_surface(X, Y, pdf, cmap=coolwarm, antialiased=False)
    print(rate.shape, e_rate.shape, pdf.shape)
    c = ax.contourf(np.log(rate),
                    np.log(e_rate),
                    (np.log(pdf) + log_xy).T,
                    levels=np.linspace(-100, np.max(np.log(pdf)+log_xy)),
                    cmap=cmap)
    ax.axvline(x=-4.68300335940118)
    ax.axvline(x=-4.665307683572091)
    ax.axvline(x=-4.701017821785233)
    fig.colorbar(c, label='natural log of pdf')
    ax.set_xlabel('detection rate (natural log)')
    ax.set_ylabel('error rate (natural log)')
    plt.show(block=False)
