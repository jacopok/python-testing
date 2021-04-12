from astroquery.nist import Nist
import scipy.constants as sc
from astropy.constants import codata2018 as ac
from astropy.constants import iau2015 as aa
import astropy.units as u
from astropy.cosmology import Planck15 as cosmo
import astropy.uncertainty as aun
import re
import numpy as np
from tqdm import tqdm

# return all digits, ignore everything else
def dig(arr):
  return_arr = []
  for x in arr:
    try:
      string = re.sub('\D', '', x)
    except (TypeError):
      return_arr.append(0.)
      continue
    try:
      return_arr.append(float(string))
    except (ValueError):
      return_arr.append(0.)
  return (return_arr)

# for sorting a list of some floats and some masked array items
def float_or(x, maximum):
  if np.ma.is_masked(x):
    return (maximum + 1)
  else:
    return(float(x))


def find_candidate_ions(wavelengths, errors):
  ranges = []
  if errors is None:
    errors = wavelengths / 200
  for w, e in zip(wavelengths, errors):
    ranges.append((w - e, w + e))
  
  tables = []
  for r in ranges:
    tables.append(Nist.query(*r, linename="All spectra"))

  sets = []
  for t in tables:
    ions = t['Spectrum']
    sets.append(set(ions))
  
  common = list(set.intersection(*sets))
  return (common)

def ion_goodness(ion, wls, N, verbose=False):
  delta = max(wls) - min(wls)
  if delta == 0:
    delta = max(wls) / 20
  range = (min(wls) - delta / 5, max(wls) + delta / 5)

  table = Nist.query(*range, linename=ion)
  table['Rel.'] = dig(table['Rel.'])
  max_int = max(table['Rel.'])
  table.sort('Rel.', reverse=True)
  first_N_wls = table[:N]['Observed']

  dist=0
  for w in wls.value:
    pos = np.argmin(np.abs(first_N_wls - w))
    dist += np.abs(first_N_wls - w)[pos]
    if (verbose):
      print(f'For wavelength {w} nm found line at:')
      print(f'{first_N_wls[pos]} nm')
      print(f'with intensity {100 * table[pos]["Rel."] / max_int:.4f}% of the max')
      print()
    first_N_wls.mask[pos] = True 
  
  return (dist)

# use this!
def find_ion(wavelengths, errors=None, N=None):
  """
  Finds the ion which most likely explains the spectral lines given.

  Arguments:
  wavelengths: array of Quantity from astropy.
  Must be convertible to wavelength with the "spectral" astropy equivalencies
  wavelengths of the lines observed

  errors: array of Quantity from astropy, with the same length as wavelengths
  Must be convertible to wavelength with the "spectral" astropy equivalencies
  in the first search, lines are sought between 
  wavelength +- error
  if None (default), errors is set as wavelengths / 200

  N: for each ion, we look at the N brightest lines in the range of interest
  if None (default), N is set to three times the number of wavelengths given
  """
  if N is None:
    # will look at the N most intense lines
    N = len(wavelengths) * 3
  print('Looking for candidate ions')
  wavelengths = wavelengths.to(u.nm, equivalencies=u.spectral())
  if errors is not None:
    errors = errors.to(u.nm, equivalencies=u.spectral())
  candidate_ions = find_candidate_ions(wavelengths, errors)
  num = len(candidate_ions)
  if num>1:
    print(f'Found {num} candidates')
  elif num == 1:
    print('Found one candidate: the following comparison is not meaningful')
  else:
    print('Found no candidates')
    return(None)

  print('Checking goodness')
  maximum = 0.
  goodnesses = {}
  for ion in tqdm(candidate_ions):
    goodnesses[ion] = ion_goodness(ion, wavelengths, N)
    maximum = max(goodnesses[ion], maximum)
  
  # sort dict of ion -> goodness
  goodnesses = {k: v for k, v in sorted(goodnesses.items(), key=lambda item: float_or(item[1], maximum))}

  i = next(iter(goodnesses))
  print(f'Best ion: {i}')
  ion_goodness(i, wavelengths, N, verbose=True)

  print(goodnesses)
  return(i)