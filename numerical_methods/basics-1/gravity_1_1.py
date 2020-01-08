import numpy as np
from astropy import constants

g = constants.g0.value # m*s**(-2)

t = float(input("Please input the time t in seconds "))
h = float(input("Please input the height h in metres "))

x = 1/2 * g * t**2
print(f"x = {x}")

t2 = np.sqrt(2*g/h)
print(f"t_2 = {t2}")