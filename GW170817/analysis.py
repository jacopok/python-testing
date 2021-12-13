#%%

import h5py
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

with h5py.File('GW170817_GWTC-1.hdf5') as file:
    
    post_ls = np.vstack((
        np.array(file['IMRPhenomPv2NRT_lowSpin_posterior']['lambda1']),
        np.array(file['IMRPhenomPv2NRT_lowSpin_posterior']['lambda2']),
    ))
    prior_ls = np.vstack((
        np.array(file['IMRPhenomPv2NRT_lowSpin_prior']['lambda1']),
        np.array(file['IMRPhenomPv2NRT_lowSpin_prior']['lambda2']),
    ))
    
    
    post_hs = np.vstack((
        np.array(file['IMRPhenomPv2NRT_highSpin_posterior']['lambda1']),
        np.array(file['IMRPhenomPv2NRT_highSpin_posterior']['lambda2']),
    ))
    prior_hs = np.vstack((
        np.array(file['IMRPhenomPv2NRT_highSpin_prior']['lambda1']),
        np.array(file['IMRPhenomPv2NRT_highSpin_prior']['lambda2']),
    ))

print('Low spin: ')
print(np.log2(gaussian_kde(post_ls, bw_method=1e-1)([0, 0]) * 2500**2)[0])
print('bits for the no-tides hypothesis')
print('High spin:')
print(np.log2(gaussian_kde(post_hs, bw_method=1e-1)([0, 0]) * 2500**2)[0])
print('bits for the no-tides hypothesis')
# %%

plt.hist2d(*post_ls, bins=200)
plt.xlim(0, 1000)
plt.ylim(0, 1000)
# %%
plt.hist2d(*post_hs, bins=200)
plt.xlim(0, 1000)
plt.ylim(0, 1000)

# %%

def plot_bw_selection(data):
    training = data[:, 1000:]
    testing = data[:, :1000]
    
    bws = np.logspace(-3, 1)
    
    entropies = [
        sum(-np.log(gaussian_kde(training, bw_method=bw)(testing)))
        for bw in bws
    ]
    plt.loglog(bws, entropies)
    
    return bws[np.argmin(entropies)]

print(plot_bw_selection(post_ls))
print(plot_bw_selection(post_hs))


# %%
_ = plt.hist2d(*prior_ls, bins=100)

# %%

_ = plt.hist2d(*prior_hs, bins=100)
# %%
