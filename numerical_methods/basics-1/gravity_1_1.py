import numpy as np
from astropy import constants
from astropy import units as u

g = constants.g0  # reference value for the gravitational acceleration 
# on the surface of the Earth

t = float(input("Please input the time t in seconds: ")) * u.s

x = (1./2. * g * t**2).to('m')
print(f"The distance fallen in {t} is {x}")

h = float(input("Please input the height h in metres: ")) * u.m

t2 = np.sqrt(2*h/g)
print(f"The time taken to fall a distance {h} is {t2}")