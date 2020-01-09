import astropy.constants as ac 

tau_th = (ac.GM_sun * ac.M_sun / ac.L_sun / ac.R_sun)
tau_dyn = np.sqrt(ac.R_sun ** 3 / ac.GM_sun)

eps = 7e-3
H_frac = 1e-1

tau_nuc = eps * ac.c**2 * H_frac * ac.M_sun / ac.L_sun