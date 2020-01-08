#%%

import matplotlib.pyplot as plt

import numpy as np

# %%

classes = np.arange(10)
# numeri da 0 a 9

freqs = classes**2
# operazione a caso

plt.bar(classes, height=freqs)

#%%
