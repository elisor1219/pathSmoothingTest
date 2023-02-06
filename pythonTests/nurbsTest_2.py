# Written with python version 3.11.1
# Reference: 1) 'The NURBS Book' by Piegl and Tiller, 2nd edition
#            2) 'NURBS Demo - Evaluator for Non Uniform Rational B-Splines' accessed 2023-02-04
#                  found at: http://nurbscalculator.in/
#            3) 'If You Know B-Splines Well, You Also Know NURBS!' by J.Fisher, J.Lowther, C.Shene
#            4) 'Non-uniform rational B-spline' by Wikipedia, accessed 2023-02-04
#                  found at: https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline
#            5) 'Path Smoothing Techniques in Robot Navigation: State-of-the-Art,
#                  Current and Future Challenges' by A.Ravankar, A.Ravankar, Y.Kobayashi,
#                  Y.Hoshino, C.Peng 

import time
import numpy as np
import matplotlib.pyplot as plt

def findSpan(n,p,u,U):
    # Algorithm A2.1 from 'The NURBS Book'
    # Determine the knot span index
    # Input: n, p, u, U
    # Output: i

    # Special cases
    if u == U[n+1]:
        return n

    # Binary search
    low = p
    high = n + 1
    mid = int((low + high)/2)

    while (u < U[mid] or u >= U[mid+1]):
        if u < U[mid]:
            high = mid
        else:
            low = mid
        mid = int((low + high)/2)
    return mid

def basisFuns(i,u,p,U):
    # Algorithm A2.2 from 'The NURBS Book'
    # Compute the nonvanishing basis functions
    # Input: i, u, p, U
    # Output: N

    # Initialize N as a None array
    N = np.empty((p+1), dtype=object)

    # Initialize left and right as a None array
    left = np.empty((p+1), dtype=object)
    right = np.empty((p+1), dtype=object)

    N[0] = 1
    for j in range(1,p+1):
        left[j] = u - U[i+1-j]
        right[j] = U[i+j] - u
        saved = 0
        for r in range(0,j):
            temp = N[r] / (right[r+1] + left[j-r])
            N[r] = saved + right[r+1] * temp
            saved = left[j-r] * temp
        N[j] = saved
    return N

def CurvePoint(n,p,U,Pw,u):
    # Algorithm A3.1 from 'The NURBS Book'
    # Compute point on rational B-spline curve
    # Input: n, p, U, Pw, u
    # Output: C
    span = findSpan(n,p,u,U)
    N = basisFuns(span,u,p,U)

    Cw = 0
    for j in range(0,p+1):
        Cw = Cw + N[j] * Pw[span-p+j,:]
    w = Cw[2]
    C = Cw / w
    # Remove the last element of C
    C = np.delete(C, 2)
    return C

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# -------------------- Input data ------------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# <-- Means that this is the input data
isBspline = True #                                <-- Is this a B-spline curve?
plt.figure()
plt.axis([0, 10, -5, 5])
plt.grid(True)
P = plt.ginput(-1, -1) #                                   <-- Control points
P = np.array(P)
#P = np.array([(0,0), (1,1), (3,2), (6,-2), (7,3), (7,2), (8,-1), (10, 7)]) #                <-- Control points
n = P.shape[0] - 1
if isBspline:
    w = np.ones((n+1))
else:
    w = np.array([1, 0.5, 5, 5, 1]) #             <-- Weights (depends on isBspline)
p = 3 #                                                 <-- Degree of the curve
# Auto determine the knots
autoDeterminKnots = True #                         <-- Auto determine the knots

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# -------------------- Main program ----------------- #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Early error checking
if n < 0:
    print('Error: n must be nonnegative')
    exit()

if p < 0:
    print('Error: p must be nonnegative')
    exit()

if p > n:
    print('Error: p must be less than or equal to n')
    exit()

# The number of Knots is r+1
r = n + p + 1 
# We want to clamp the end knots, so the first p+1 knots are equal to 0 and
# the last p+1 knots are equal to 1 
UStart = np.zeros((p+1))
UEnd = np.ones((p+1))
# UMid is of size n - p
if autoDeterminKnots:
    UMid = np.linspace(0,1,n-p+2)
    UMid = np.delete(UMid, 0)
    lastUMidIndex = UMid.shape[0]-1
    UMid = np.delete(UMid, lastUMidIndex)
else:
    print('n-p = ', n-p)
    UMid = [0.5]
U = np.concatenate((UStart, UMid, UEnd))
m = U.shape[0] - 1

# Error checking
if w.shape[0] != n+1:
    print('Error: w must have the same length as P')
    print('Size of w = ', w.shape[0])
    print('Size of P = ', P.shape[0])
    print('You could increase the size of w by', n+1-w.shape[0], 'element(s)')
    exit()


if U.shape[0] != r + 1:
    print('Error: U must have length ', r+1)
    print('Size of U = ', U.shape[0])
    if U.shape[0] < r + 1:
        print('You could increase the size of UMid by', r+1-U.shape[0], 'element(s)')
    else:
        print('You could decrease the size of UMid by', U.shape[0]-r-1, 'element(s)')
    exit()


Pw = np.zeros((n+1,3))
for i in range(0,n+1):
    Pw[i,0] = P[i,0]*w[i]
    Pw[i,1] = P[i,1]*w[i]
    Pw[i,2] = w[i]

u = np.linspace(0,max(U),100)
C = np.zeros((u.shape[0],P.shape[1]))

t = time.time()
for inx in range(0,u.shape[0]):
    C[inx,:] = CurvePoint(n,p,U,Pw,u[inx])

#print('Time elapsed = ', time.time() - t)

plt.figure()
if isBspline:
    plt.title('B-spline curve')
else:
    plt.title('Rational B-spline curve')

plt.plot(C[:,0], C[:,1], label='Curve point of degree ' + str(p))
plt.plot(P[:,0], P[:,1], 'o--', label='Control points')
plt.legend()
plt.show()

