import sympy as sym
sym.init_printing()

R, r, a, ut, uphi, e, l = sym.symbols('R r a ut uphi e l')

coeffs = sym.Matrix([
    [1 - 1 / R, -a / R],
    [-a/R, r**2 + a**2 *(1 + 1/R)]
])

print(sym.simplify(coeffs.inv()))