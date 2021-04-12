p = .3 * sc.atmosphere * u.Pa
rho = 1e3 * u.kg / u.m**3
v0 = 2 *u.m / u.s
v = np.sqrt(2 * p/rho - v0**2)
v
v.to('m/s')
v = np.sqrt(2 * p/rho + v0**2)
v.to('m/s')
np.sqrt(p/rho)
np.sqrt(p/rho).to('m/s')
p
rho
8.04953
8.04953 *(1 + 0.05/100)
8.04953 *(1 - 0.05/100)
%history

