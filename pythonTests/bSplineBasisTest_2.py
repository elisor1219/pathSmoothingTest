# Written with python version 3.11.1
import time
import numpy as np
import matplotlib.pyplot as plt

def OneBasisFun(p, m, U, i, u):
    # Compute the basis function Nip
    # Input: p, m, U, i, u
    # Output: Nip

    # Special cases
    if ((i == 0 and u == U[0]) or (i == m-p-1 and u == U[m])):
        Nip = 1
        return Nip
    
    #Local property
    if (u < U[i] or u >= U[i+p+1]):
        Nip = 0
        return Nip
    
    # Initialize N as a None array
    N = np.empty((p+1), dtype=object)

    # Initialize zeroth-degree functs
    for j in range(0,p+1):
        if (u >= U[i+j] and u < U[i+j+1]):
            N[j] = 1
        else:
            N[j] = 0

    # Compute triangular table
    for k in range(1,p+1):
        if (N[0] == 0):
            saved = 0
        else:
            saved = ((u - U[i]) * N[0]) / (U[i+k] - U[i])

        for j in range(0,p-k+1):
            Uleft = U[i+j+1]
            Uright = U[i+j+k+1]

            if (N[j+1] == 0):
                N[j] = saved
                saved = 0
            else:
                temp = N[j+1] / (Uright - Uleft)
                N[j] = saved + (Uright - u) * temp
                saved = (u - Uleft) * temp
    Nip = N[0]
    return Nip

p = 2
U = np.array([0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 5])
m = U.shape[0] - 1
u = 5/2

i = 4
deg = 2

t = time.time()
print(OneBasisFun(deg, m, U, i, u))
print(time.time() - t)

