import numpy as np
import matplotlib.pyplot as plt

# all numbers are in SI units

def seglen_from_freq(f):
    return 180 * (f / 20)**(-8/3)

def default_fft_grid(f_min, f_max):
    seglen = seglen_from_freq(f_min) 
    return np.arange(f_min, f_max, step=1 / seglen)

def reduced_grid(f_min, f_max, f_crit=30.):

    EXTRA_FACTOR = 1.

    if f_max > f_crit:
        high_frequency_grid = np.arange(f_crit, f_max, step=1/seglen_from_freq(f_crit)/EXTRA_FACTOR)
        if f_min > f_crit:
            return high_frequency_grid
        low_frequency_grid = reduced_grid(f_min, f_crit)
        return np.append(
            low_frequency_grid, 
            np.arange(f_crit, f_max, step=1/seglen_from_freq(f_crit)/EXTRA_FACTOR)
            )

    f_min_reduced, f_max_reduced = f_min**(-5/3), f_max**(-5/3)
    grid = np.arange(f_max_reduced, f_min_reduced, step=1/seglen_from_freq(1) * (5/3)/EXTRA_FACTOR)
    
    return grid**(-3/5)


def plot_sample_density():
    
    # F_MIN, F_MAX = 10., 2048.
    F_MIN, F_MAX = 10., 100.
    
    fft_grid = default_fft_grid(F_MIN, F_MAX)
    my_grid = reduced_grid(F_MIN, F_MAX)
    
    plt.hist(fft_grid, 
            bins=np.arange(F_MIN, F_MAX+1), 
            alpha=.5, 
            label=f'Default FFT grid ({len(fft_grid)})')

    plt.hist(my_grid, 
            bins=np.arange(F_MIN, F_MAX+1), 
            alpha=.5, 
            label=f'Reduced grid ({len(my_grid)})')
    
    plt.plot(fft_grid, seglen_from_freq(fft_grid), label='0PN expected seglen')
    
    plt.ylabel(r'Frequency sample density $d N / d f$ or seglen [1/Hz]')
    plt.xlabel('Frequency [Hz]')
    plt.legend(loc='upper right')
    # plt.xscale('log')
    # plt.yscale('log')
    plt.savefig('frequency_multibanding.pdf')
    
def plot_n_points_scaling():
    for f_crit in [20, 30, 40, 50]:
        f_mins = np.linspace(1, 20, dtype=int)
        
        plt.plot(f_mins, [len(reduced_grid(f_min, 2048., f_crit)) for f_min in f_mins], label=f_crit)
        _, upper_lim = plt.ylim()
        plt.ylim((0, upper_lim))
    plt.legend()
    plt.show()

if __name__ == '__main__':
    plot_sample_density()
    # plot_n_points_scaling()