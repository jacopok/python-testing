import sympy as sym
sym.init_printing()

x, y = sym.symbols('x y')

variables = [x, y]

metric = sym.Matrix([
  [1 + 4*x** 2, -4*x*y],
  [-4 * x * y, 1 + 4 * y**2]
])

def Christoffel(metric, variables):
  m, n = metric.shape
  if (m != n):
    print("Rectangular metric!")
    return (None)
  
  inverse_metric = metric.inv()

  