import numpy as np

# linear transformation between
# metric derivatives and Christoffel symbols
M = np.zeros((4**3, 4**3))

# three indices run from 0 to 3:
# we incorporate them into one
# from 0 to 4**3-1
d = lambda i,j,k: 4**2*i+4*j+k

# we populate the metric with the relevant coefficients,
# starting from the formula 
# Γ_μνρ = 1/2(g_μν,ρ + g_μρ,ν - g_νρ,μ)
# we neglect the 1/2 in order to have
# less numerical noise, and a clearer view
# of the fact that the determinant is nonzero
for i in range(4):
    for j in range(4):
        for k in range(4):
            M[d(i, j, k), d(i, j ,k)] += 1
            M[d(i, j, k), d(i, k, j)] += 1
            M[d(i, j, k), d(k, j, i)] += -1

print(np.linalg.det(M))