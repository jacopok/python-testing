import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

tot_days = 25

n = np.arange(0,2 *tot_days)

rs = 2 - n / tot_days

xs = [1]
ds = [1]

for r in rs:
  new_d = r * ds[-1]
  ds.append(new_d)

for d in ds:
  new_x = xs[-1] + d
  xs.append(new_x)

plt.plot(n, rs)
plt.plot(n, ds[1:])
plt.plot(n, xs[2:])
plt.show(block=False)