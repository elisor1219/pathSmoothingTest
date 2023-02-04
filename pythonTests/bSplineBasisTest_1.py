# Written with python version 3.11.1
import time
import numpy as np
import matplotlib.pyplot as plt

t = time.time()

# n+1 control points
P = np.matrix([[0.0, 0.0], [1.0, 2.0], [2.0, 3.0], [4.0, 0.0]])     #<---Input
n = P.shape[0] - 1

# degree p 
p = 3                                                               #<---Input

# m+1 knot vector
m = n + p + 1
U = np.linspace(0, 1, m+1 - 2*p)
U = np.concatenate((np.zeros(p), U, np.ones(p)))

U = np.array([0, 0, 0, 0, 1, 1, 1, 1])                        #<---Input
m = U.shape[0] - 1

# weight vector
w = np.ones(n+1)                                                    #<---Input

# u
u = 0.5                                                             #<---Input

# Preallocate N matrix (order p+1)
# i = 0,...,m-1 (i x p+1 matrix)
N = np.zeros((m, p+1))

for i in range(0, n):
    if u >= U[i] and u < U[i+1]:
        N[i,0] = 1
    else: 
        N[i,0] = 0

def leftMult(i,p,u,U):
    if (U[i+p] - U[i]) == 0:
        return 0
    else:
        return (u - U[i])/(U[i+p] - U[i])

def rightMult(i,p,u,U):
    if (U[i+p+1] - U[i+1]) == 0:
        return 0
    else:
        return (U[i+p+1] - u)/(U[i+p+1] - U[i+1])

def bSplineBasis(i,p,u,U):
    if p == 0:
        if u >= U[i] and u < U[i+1]:
            return 1
        else:
            return 0
    # Every time we increase the degree, we lose one i
    if p + i >= m:
        return None

    leftMultVar = leftMult(i,p,u,U)
    rightMultVar = rightMult(i,p,u,U)

    return leftMultVar*bSplineBasis(i,p-1,u,U) + rightMultVar*bSplineBasis(i+1,p-1,u,U)

# Testing bSplineBasis

u = np.linspace(0,max(U),100)
NBig = np.empty((u.shape[0], m, p+1), dtype=object)

for index in range(0, u.shape[0]):
    for i in range(0, m):
        for deg in range(0, p+1):
            NBig[index,i,deg] = bSplineBasis(i,deg,u[index],U)
elapsed = time.time() - t

print("size of NBig = ", NBig.shape)



# Plot the b spline basis functions
plt.figure()
deg = 3
for i in range(0, m-deg):
    plt.plot(u, NBig[:,i,deg], label='N_('+str(i)+','+str(deg)+')')

plt.xlabel('u')
plt.ylabel('N')
plt.legend()
#plt.show()

print("Time elapsed = ", elapsed)

# --------------------- B spline curve ---------------------


sumTemp = 0

n = m-p-1

sum = np.zeros((u.shape[0], 2))
for index in range(0, u.shape[0]):
    sumTemp = 0
    for i in range(0, n):
        print("---------------------")
        print("i = ", i)
        N = NBig[index,i,deg]
        print("N = ", N)
        print("P = ", P[i,:])
        sumTemp += N*P[i,:]
    sum[index,:] = sumTemp

# Plot the b spline curve
plt.figure()
plt.plot(sum[:,0], sum[:,1], label='B spline curve')
plt.plot(P[:,0], P[:,1], 'o--', label='Control points')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()



