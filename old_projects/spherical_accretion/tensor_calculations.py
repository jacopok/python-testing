import sympy as sp
sp.init_printing()

w0, w1, w2, r, theta, v, M, P, rho = sp.symbols('w0 w1 w2 r theta v M P rho', real=True)
#gamma = 1/sp.sqrt(1-v**2)
gamma = sp.symbols('gamma')
#y = sp.sqrt((1-2*M/r) / (1 - v**2))
y = sp.symbols('y')

#%%

T_rad_fiducial = sp.Matrix(
[
[w0, w1, 0, 0],
[w1, w0/3 + w2, 0, 0],
[0, 0, w0/3- w2/2, 0],
[0, 0, 0, w0/3 - w2/2]]
)

T_matter_fiducial = sp.Matrix([
[rho, 0,0,0],
[0,P,0,0],
[0,0,P,0],
[0,0,0,P]
])

T_fiducial = T_matter_fiducial + T_rad_fiducial

fiducial_basis = sp.Matrix([
[gamma**2/y, -y*v, 0, 0],
[-v*gamma**2/y, y, 0, 0],
[0,0,1/r,0],
[0,0,0,1/(r*sp.sin(theta))]
])

T_spherical = sp.simplify(fiducial_basis.T * T_fiducial * fiducial_basis)

print(sp.latex(T_spherical[0:2,0:2]))
