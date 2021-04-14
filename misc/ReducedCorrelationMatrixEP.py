import math as m
import numpy as np
import time
from numba import njit


###################################################################
@njit
def Masses(i, theta, L):
    "calulates the mass in the site i for a chain of length 2L  and defect strength theta"
    if i <= L and i >= 0:
        Masses = m.exp(theta)
    elif i <= 2 * L and i >= L + 1:
        Masses = m.exp(-theta)
    else:
        print("Masses out of the Harmonic Chain!")

    return Masses


#################################################################################################################################


@njit
def Omega(n, w, L):
    "Calculates the eigenvalue of index n running from 1 to 2L, given the h.o. mass w and the half chain length L "

    if n >= 1 and n <= 2 * L:
        temp = m.cos((n - 1) * m.pi / (2 * L))
        Omega = m.sqrt(w**2 + 2 * (1 - temp))
    else:
        print("Eigenvalue out of the Harmonic Chain")

    return Omega


##################################################################################################################################


@njit
def Phi(i, n, w, L):
    "Calculates the i_th entry of the eigenvector of eigenvalue index n, given the mass w and the half length L"

    if n == 1:
        Phi = m.sqrt(1 / (2 * L))

    elif n > 1 and n <= (2 * L):
        temp = m.cos(((i - 0.5) * (n - 1) * m.pi) / (2 * L))
        Phi = m.sqrt(1 / L) * temp

    else:
        print(
            "Eigenvector went on a wrong eigenvalue index which is  out of harmonic chain"
        )
        Phi = None

    if i < 1 or i > (2 * L):
        print("Eigenvector went on an entry index out of harmonic chain")
        Phi = None

    return Phi


################################################################################################################################
@njit
def RedPosCorr2(w, theta, L):

    # start_time = time.time()

    #Masses
    m1 = m.exp(theta)
    m2 = m.exp(-theta)

    #Collect the spectrum in a vector
    Spectrum = [Omega(i, 1, L) for i in range(1, L * 2 + 1)]

    #Collect the inhomogeneous change of basis in a vector
    t = m.tanh(theta)
    t_plus = m.sqrt(1 + m.tanh(theta))
    t_minus = m.sqrt(1 - m.tanh(theta))

    # start_time = time.time()

    # middle = time.time()
    #print(middle -start_time)

    # end_time = time.time()
    #print(end_time - middle )

    P = []
    for i in range(1, L + 1):

        temp = []
        for n in range(1, 2 * L + 1):
            if (n % 2 == 1): temp.append(t_plus * Phi(i, n, w, L))
            else: temp.append(t_minus * Phi(i, n, w, L))

        P.append(temp)

    RedPosCorr = []
        #print( "Prov", prov)
        # RedPosCorr.append(prov)
	

    for i in range(L):
        prov = []
        for j in range(L):
            somma = 0.0
            for n in range(2 * L):
                somma = somma + ((P[i][n] * P[j][n]) / Spectrum[n])
                #print(n)
                #print(somma)
            prov.append(somma / (2 * m1))

        #print( "Prov", prov)
        RedPosCorr.append(prov)
	
    # print("Metodo2 \n",  len(RedPosCorr), 	len(RedPosCorr[0]))
    # end_time = time.time()
    # print("TEMPO Metodo 2", end_time - start_time )

    return RedPosCorr


################################################################################################################################

print(" Series of Omega(n,w=1,L=2) ")
L = 1
print([Omega(i, 1, L) for i in range(1, L * 2 + 1)])

print(" Series of Phi(i,n=1,w=1,L=2) ")
print(Phi(1, 1, 1, 2))
print(Phi(2, 1, 1, 2))
print(Phi(3, 1, 1, 2))
print(Phi(4, 1, 1, 2))

print(" Series of Phi(i,n=2,w=1,L=2) ")
print(Phi(1, 2, 1, 2))
print(Phi(2, 2, 1, 2))
print(Phi(3, 2, 1, 2))
print(Phi(4, 2, 1, 2))

#Intial Parameters
L = 100
w = 1
theta = 1

print("Parameters (L,w,theta) ", L, w, theta)
Spectrum = [Omega(i, 1, L) for i in range(1, L * 2 + 1)]

# in un terminale ipython:
# %timeit corr_matrix = RedPosCorr2( w, theta, L )
