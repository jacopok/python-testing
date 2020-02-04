import numpy as np
import astropy.units as u
u.set_enabled_equivalencies(u.spectral())

CENTRAL_A_FREQ = 440

notes_dict = {
  0: 'A',
  1: 'A#',
  2: 'B',
  3: 'C',
  4: 'C#',
  5: 'D',
  6: 'D#',
  7: 'E',
  8: 'F',
  9: 'F#',
  10: 'G',
  11: 'G#'
}

def energy_to_note(x, verbose=True):
  x_freq = x.to(u.Hz).value
  float_octave = np.log2(x_freq) - np.log2(CENTRAL_A_FREQ)
  octave = int(float_octave)
  note = int(np.round((float_octave - octave) * 12))
  if (verbose):
    print(f'{notes_dict[note]}{octave}')
  return (note, octave)

