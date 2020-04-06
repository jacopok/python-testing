import numpy as np
import astropy.units as u
from bayesian_hyp_testing import loguniform_dist, normal_dist, uniform_dist
import uncertainties as un
# import uncertainties.umath as um

RESOLUTION = 80.955 * u.picosecond

GATE_FREQ = 34.95490663 * u.kHz

DETECTOR_FREQ = 23.76362711 * u.kHz

DARK_COUNT = 200 * u.Hz

OBS_TIME = 1 * u.min

WINDOW_COINCIDENCE = 30 * 2 * RESOLUTION


def pv(N):
    """Poisson error on a variable"""
    return un.ufloat(N, np.sqrt(N))


N_G = pv(1_554_341)
N_1 = 1_056_698
N_2 = 1_000_384
N_G1 = pv(13_930)
N_G2 = pv(14_829)
N_G12 = 3

g = (N_G * N_G12 / (N_G1 * N_G2)).n

N_NOISE = (WINDOW_COINCIDENCE * DETECTOR_FREQ).to(1).value
RATE = (N_G1 + N_G2) / (2 * N_G)
E_RATE = N_NOISE / N_G

e_rate, e_rate_pdf = uniform_dist(-12, -2, num=100)
rate, rate_pdf = normal_dist(RATE.n, RATE.s, num=20)
# rate, rate_pdf = loguniform_dist(-8, 0, num=25)


param_prior = np.outer(rate_pdf, e_rate_pdf)

# param_prior_visible = np.outer(rate_pdf / np.gradient(rate), e_rate_pdf / np.gradient(e_rate))
