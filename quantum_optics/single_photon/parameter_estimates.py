import numpy as np
import scipy.constants as sc
from astropy.constants import codata2018 as ac
from astropy.constants import iau2015 as aa
import astropy.units as u
from astropy.cosmology import Planck15 as cosmo
import astropy.uncertainty as aun

GATE_FREQ = 34.95490663 * u.kHz

DETECTOR_FREQ = 23.76362711 * u.kHz

DARK_COUNT = 200 * u.Hz

OBS_TIME = 1 * u.min

WINDOW_COINCIDENCE = 300 * u.ns
