import time
import numpy as np
import matplotlib.pyplot as plt

from nurbsAlgorithms import CurvePoint
from nurbs import NURBS

def main():
        # <-- Means that this is the input data
    isBspline = True #                                <-- Is this a B-spline curve?
    plt.figure()
    plt.axis([0, 10, -5, 5])
    plt.grid(True)
    P = plt.ginput(-1, -1) #                                   <-- Control points
    P = np.array(P)
    n = P.shape[0] - 1
    if isBspline:
        w = np.ones((n+1))
    else:
        w = np.array([1, 0.5, 5, 5, 1]) #             <-- Weights (depends on isBspline)
    p = 3 #                                                 <-- Degree of the curve
    # Auto determine the knots
    autoDeterminKnots = True #                         <-- Auto determine the knots




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

    nurbsClass = NURBS
    C = nurbsClass.constructBezier(P, 100)

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



if __name__ == '__main__':
    main()