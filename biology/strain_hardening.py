from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy import stats

@dataclass
class StressSweep:
    # in percentage
    chitosan_concentration: float
    rdg: int
    tau: list[float]
    g_prime: list[float]
    gamma: list[float]

    def strain_hardening(self):
        minimum = min(self.g_prime[:-1])
        maximum = max(self.g_prime)
        return maximum / minimum

    def shear_modulus_fit_results(self, maximum_gamma=0.05):
        index = np.searchsorted(self.gamma, maximum_gamma)
        return stats.linregress(self.gamma[:index], self.tau[:index])
    
    def shear_modulus(self, maximum_gamma=0.05):
        return self.shear_modulus_fit_results(maximum_gamma).slope

    def shear_modulus_fit_rvalue(self, maximum_gamma=0.05):
        return self.shear_modulus_fit_results(maximum_gamma).rvalue

def plot_sweeps(list_of_sweeps: list[StressSweep]):
    """Given a list of sweeps, makes a scatter plot
    with two x axes --- chitosan concentration and RDG --- 
    and saves it to "chitosan.pdf".
    """
    chitosan_concentrations = [sw.chitosan_concentration for sw in list_of_sweeps]
    rdgs = [sw.rdg for sw in list_of_sweeps]
    shear_moduli = [sw.shear_modulus() for sw in list_of_sweeps]
    strain_hardenings = [sw.strain_hardening() for sw in list_of_sweeps]

    plt.scatter(chitosan_concentrations, strain_hardenings, alpha=0.)
    cmap = plt.get_cmap('plasma')
    norm = mpl.colors.Normalize(vmin=min(shear_moduli), vmax=max(shear_moduli))

    ax = plt.gca()
    ax.grid('on')
    ax.set_xlabel('Chitosan concentration [percent]')
    ax.set_ylabel('Strain hardening [dimensionless]')

    new_ax = ax.twiny()
    colors = new_ax.scatter(rdgs, strain_hardenings, c=shear_moduli, cmap=cmap, norm=norm, s=80.)
    new_ax.set_xlabel('RDG [mol/mol]')
    new_ax.set_xticks(rdgs)
    
    cbar = plt.colorbar(mappable=colors, label='Shear modulus [Pa]', ticks=shear_moduli)

    plt.savefig('chitosan.pdf')
