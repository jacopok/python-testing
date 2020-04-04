import numpy as np
import astropy.units as u

RESOLUTION = 81 * u.picosecond

GATE_FREQ = 34.95490663 * u.kHz

DETECTOR_FREQ = 23.76362711 * u.kHz

DARK_COUNT = 200 * u.Hz

OBS_TIME = 1 * u.min

WINDOW_COINCIDENCE = 30 * 2 * RESOLUTION

N_G = 1_554_341
N_1 = 1_056_698
N_2 = 1_000_384
N_G1 = 13_930
N_G2 = 14_829
N_G12 = 3

g = N_G * N_G12 / (N_G1 * N_G2)

N_NOISE = (WINDOW_COINCIDENCE * DETECTOR_FREQ).to(1).value
RATE = (N_G1 + N_G2) / (2 * N_G)
E_RATE = N_NOISE / N_G

