from gauss_seidel import gauss_seidel
import numpy as np

"""
The system can be solved by just writing out the
node equations at the 4 nodes; if we simplify the 
resistence we get that the matrix multiplying the
vector (V_i) with i=1..4 is found by 
putting on the diagonal entry corresponding to each element
the number of connections it has, 
and then putting a -1 on each entry to which it is connected, plus possibly a V+ if it is also connected 
to V+.
"""
A = np.array([
    [4, -1, -1, -1],
    [-1, 3, 0, -1],
    [-1, 0, 3, -1],
    [-1, -1, -1, 4]
])

"""
while the vector b is:
"""
V_plus = 5

b = np.array([1, 0, 1, 0]) * V_plus

"""
so we can solve the system with the Gauss-Seidel method: 
the kind of circuit guarantees that the matrix is (not strictly) diagonally dominant, since the diagonal entries must equal the number of ones on the row (counting a one also if there is a V+ on the rame row of b)
"""

x, n = gauss_seidel(A, b)
print(x)    