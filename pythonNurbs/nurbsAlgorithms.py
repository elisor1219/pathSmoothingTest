import numpy as np

def findSpan(n,p,u,U):
    # Algorithm A2.1 from 'The NURBS Book'
    # Determine the knot span index
    # Input: n, p, u, U
    # Output: i

    # Special cases
    threshold = 1e-10
    if abs(u - U[n+1]) < threshold:
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