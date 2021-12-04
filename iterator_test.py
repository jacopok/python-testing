#%%
import numpy as np
import matplotlib.pyplot as plt

lim_k_dex = 1
N_plotted=100

def cubic(x, center=0, width=2*lim_k_dex):
    return (width/2)**(-3) * (abs(x - center))**1.5 * np.sign(x-center)
    
def inverse_cubic(y, center=0, width=lim_k_dex):
    return center + (y)**(1/3) * (width/2)

logs = cubic(np.linspace(-lim_k_dex, lim_k_dex, num=N_plotted))

plt.plot(logs)

# %%
