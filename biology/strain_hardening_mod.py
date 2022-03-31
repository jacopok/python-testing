from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from typing import List
from scipy import stats, optimize

@dataclass
class FrequencySweep:
    frequency: List[float]
    g_prime: List[float]
    g_second: List[float] 
    maximum_freq: float=15
    
    def freq_mask(self):
        return np.array(self.frequency)<self.maximum_freq
            
    def shear_modulus(self):
        def error (x):
            ge, l1, e1, e2=x
            freq=np.array(self.frequency)[self.freq_mask()]
            omega=2*np.pi*np.array(freq)
            ei_list=[e1, e2]
            g_prime_cut=np.array(self.g_prime)[self.freq_mask()]
            g_second_cut=np.array(self.g_second)[self.freq_mask()]
            g_prime_theo=ge*np.ones_like(freq)
            g_second_theo=np.zeros_like(freq)
            for i, ei in enumerate(ei_list):
                li=l1*(10**i)
                g_prime_theo+=(ei/li)*((li*omega)**2/(1+(li*omega)**2))
                g_second_theo+=(ei/li)*(li*omega)/(1+(li*omega)**2)
            g_prime_err=np.sum((g_prime_theo-g_prime_cut)**2)
            g_second_err=np.sum((g_second_theo-g_second_cut)**2)
            return g_prime_err+g_second_err
        res=optimize.minimize(error, x0= [154, 0.01, 23, 18],
                              bounds=[(1e-6,np.inf) for _ in range(4)],
                              method="Nelder-Mead"
                              )
        
        print (res)
        ge, l1, e1, e2=res.x
        ei_list=[e1, e2]
        gi_sum=sum(e/(l1*10**i) for i,e in enumerate(ei_list))
        return ge+gi_sum
     
            
            
@dataclass
class StressSweep:
    tau: List[float]
    g_prime: List[float]
    gamma: List[float]
    maximum_gamma: float = 0.05

    def maximum_gamma_index(self):
        return np.searchsorted (self.gamma, self.maximum_gamma)
        
    def strain_hardening(self): 
        linear_mean = np.mean(self.g_prime[:self.maximum_gamma_index()])
        maximum = max(self.g_prime)
        return maximum / linear_mean

    def shear_modulus_fit_results(self):
        index = self.maximum_gamma_index()
        return stats.linregress(self.gamma[:index], self.tau[:index])
    
    def shear_modulus_approx(self):
        return self.shear_modulus_fit_results().slope

    def shear_modulus_fit_rvalue(self):
        return self.shear_modulus_fit_results().rvalue

@dataclass
class Sample:
    chitosan_concentration: float  
    rdg: int
    stress_sweep: StressSweep
    frequency_sweep: FrequencySweep

def plot_sweeps(list_of_sweeps: List[StressSweep]):
    """Given a list of sweeps, makes a scatter plot
    with two x axes --- chitosan concentration and RDG --- 
    and saves it to "chitosan.pdf".
    """
    chitosan_concentrations = [sw.chitosan_concentration for sw in list_of_sweeps]
    rdgs = [sw.rdg for sw in list_of_sweeps]
    shear_moduli = [sw.shear_modulus() for sw in list_of_sweeps]
    strain_hardenings = [sw.strain_hardening() for sw in list_of_sweeps]
 

    plt.scatter(chitosan_concentrations, shear_moduli, alpha=0.)
    cmap = plt.get_cmap('plasma')
    norm = mpl.colors.Normalize(vmin=(min(strain_hardenings)-0.1), vmax=(max(strain_hardenings)+0.1))

    ax = plt.gca()
    ax.grid('on')
    ax.set_xlabel('Chitosan concentration [m/V, %]')
    ax.set_ylabel('Shear modulus [Pa]')

    new_ax = ax.twiny()
    colors = new_ax.scatter(rdgs, shear_moduli, c=strain_hardenings, cmap=cmap, norm=norm, s=80.)
    new_ax.set_xlabel('R D/G')
    new_ax.set_xticks(rdgs)
    
    def tick_format(position, tick_number):
        return f'{position:.1f}'
    
    cbar = plt.colorbar(mappable=colors, label='Strain hardening', ticks=strain_hardenings, format=tick_format)

    plt.savefig('chitconc.pdf')

