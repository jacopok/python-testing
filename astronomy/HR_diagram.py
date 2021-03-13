#%%
import numpy as np
from astropy.time import Time
import astropy.units as u
from astropy.coordinates import get_icrs_coordinates
import astroquery
from astroquery.simbad import Simbad
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from astropy.coordinates import SkyCoord


# %%

orion_stars = [
    'Betelgeuse',
    'Rigel',
    'Bellatrix',
    'Mintaka',
    'Alnilam',
    'Alnitak',
    'Saiph',
    'Meissa',
]

mags = [
    .45, .15, 1.6, 2.4, 1.65, 1.85, 2.05, 3.5
]

Simbad.reset_votable_fields()
Simbad.add_votable_fields('flux(B)', 'flux(V)')
Simbad.add_votable_fields('parallax')

#%%

B_mag = []
V_mag = []
plx = []
coords = []

for star in orion_stars:
    simbad_data = Simbad.query_object(star)
    B_mag.append(simbad_data['FLUX_B'].data[0])
    V_mag.append(simbad_data['FLUX_V'].data[0])
    plx.append(simbad_data['PLX_VALUE'].data[0])  # mas
    coords.append([simbad_data['RA'].data[0], simbad_data['DEC'].data[0]])

B_mag = np.array(B_mag)
V_mag = np.array(V_mag)
plx = np.array(plx)
dist_pc = 1000 / (plx)
mag_correction = - 5 * (np.log10(dist_pc) - 1)

ast_coords = []

for c, d in zip(coords, dist_pc):
    ast_coords.append(SkyCoord(ra=c[0], dec=c[1], unit=(u.hourangle, u.deg), distance = d * u.pc).cartesian)

# %%

for (B, V, mag, name) in zip(B_mag, V_mag, mags, orion_stars):
    x = B - V
    y = mag
    print(x, y)
    plt.scatter(x, y)
    plt.annotate(name, xy=(x, y), xytext=(3, 3), textcoords='offset points')
    
plt.ylim(plt.ylim()[::-1])
plt.xlabel('Colore (blu $\\to$ rosso) o temperatura (caldo $\\to$ freddo)')
plt.ylabel('Magnitudine apparente')
plt.savefig('pics/rel_mag.png', dpi=150)

# %%

print(np.average(mag_correction))
mag_correction -= np.average(mag_correction)

for (B, V, name, mag, mc) in zip(B_mag, V_mag, orion_stars, mags, mag_correction):
    x = B - V
    y0 = mag 
    y = y0 + mc
    plt.scatter(x, y)
    plt.annotate(name, xy=(x, y), xytext=(3, 3), textcoords='offset points')
    color = 'green' if mc < 0 else 'red'
    plt.arrow(x, y0, 0, mc, color=color, alpha=.3)
    
plt.ylim(plt.ylim()[::-1])
plt.xlabel('Colore (blu $\\to$ rosso) o temperatura (caldo $\\to$ freddo)')
plt.ylabel('Magnitudine vera')
plt.savefig('pics/abs_mag.png', dpi=150)

# %%

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()

ax = Axes3D(fig)

for c in ast_coords:
    ax.scatter(c.x, c.y, c.z)
plt.show()
# %%
