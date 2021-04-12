#%%

import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)

def d():
    print('called d')
    while True:
        ds = np.random.randint(1, 7, 2)
        yield np.sum(ds) % 6 + 1

gen = d()
x = [next(gen) for n in range(10000)]
plt.hist(x, bins=np.arange(6) + .5)

# %%
