import numpy as np
import matplotlib.pyplot as plt

def BasisFuns(i, u, p, U):
    N = [0.0 for k in range(p+1)]
    N[0] = 1.0
    left = [0.0 for k in range(p+1)]
    right = [0.0 for k in range(p+1)]
    for j in range(1, p+1):
        left[j] = u - U[i+1-j]
        right[j] = U[i+j] - u
        saved = 0.0
        for r in range(j):
            temp = N[r]/(right[r+1] + left[j-r])
            N[r] = saved + right[r+1]*temp
            saved = left[j-r]*temp
        N[j] = saved
    return N

def FindSpan(n, p, u, U):
    if u == U[n+1]:
        return n
    low = p
    high = n+1
    mid = np.floor((low+high)/2).astype(int)
    while u < U[mid] or u >= U[mid+1]:
        if u < U[mid]:
            high = mid
        else:
            low = mid
        mid = np.floor((low+high)/2).astype(int)
        print(mid)
    return mid

def CurvePoint(n, p, U, Pw, u):
    span = FindSpan(n, p, u, U)
    N = BasisFuns(span, u, p, U)
    Cw = [0.0 for k in range(4)]
    for j in range(p+1):
        Cw[0] += N[j]*Pw[span-p+j][0]
        Cw[1] += N[j]*Pw[span-p+j][1]
        Cw[2] += N[j]*Pw[span-p+j][2]
        Cw[3] += N[j]*Pw[span-p+j][3]
    C = [0.0 for k in range(3)]
    C[0] = Cw[0]/Cw[3]
    C[1] = Cw[1]/Cw[3]
    C[2] = Cw[2]/Cw[3]
    return C

# Set some values
n = 3
p = 2
U = [0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0]
Pw = [[1.0, 0.0, 0.0, 1.0], [2.0, 0.0, 0.0, 1.0], [3.0, 0.0, 0.0, 1.0], [4.0, 0.0, 0.0, 1.0]]
u = 1.5

# Calculate the point
C = CurvePoint(n, p, U, Pw, u)
print(C)

# Plot the curve
#u = np.linspace(0.0, 3.0, 100)
#C = [CurvePoint(n, p, U, Pw, ui) for ui in u]
#plt.plot([Pw[i][0] for i in range(n+1)], [Pw[i][1] for i in range(n+1)], 'ro')
#plt.plot([C[i][0] for i in range(len(u))], [C[i][1] for i in range(len(u))], 'b-')

plt.xlabel('x')
plt.ylabel('y')
plt.show()