# %%

import numpy as np
import matplotlib.pyplot as plt

ptot = 1.

N = int(1e2)

logit_pA = np.linspace(-3, 3)

pA = ptot * np.exp(logit_pA) / (1 + np.exp(logit_pA))
pB = ptot-pA

logO = np.log(pA / pB)

sigmalogO = 1 / np.sqrt(N) * np.sqrt(1/pA + 1/pB)
sigmalogO2 = 1 / np.sqrt(N) * np.sqrt(pA/(1-pA) + pB/(1-pB))

plt.plot(pA, logO, label='estimated log-odds')

for sigmas in [3]:
    label = f'my $3\\sigma$ contour for N={N}' if sigmas == 3 else ''
    plt.fill_between(pA, logO-sigmas*sigmalogO, logO +
                     sigmas*sigmalogO, alpha=.3, color='blue', label=label)

for sigmas in [3]:
    label = f'paper $3\\sigma$ contour for N={N}' if sigmas == 3 else ''
    plt.fill_between(pA, logO-sigmas*sigmalogO2, logO +
                     sigmas*sigmalogO2, alpha=.3, color='red', label=label)


# plt.axvline(ptot, label='$p _{\\mathrm{tot}}$', c='black', ls=':')

# plt.plot(pA, sigmalogO / sigmalogO2)

plt.xscale('logit')
plt.xlabel('$p_A = p _{\\mathrm{tot}} - p_B$')
plt.ylabel('$\\log \\mathcal{O}$ [nats]')
plt.legend(loc='upper left')
# plt.yscale('log')

plt.savefig('compared-threesigma-2.pdf', dpi=150)

# %%

plt.close()
# %%

# %%
