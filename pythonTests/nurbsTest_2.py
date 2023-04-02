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

    if True:
        threshold = 1e-5
        # Special cases

        if u >= U[n+1]:
            print("What are you doing here? u = ", u)

        if  abs(U[n+1] - u) < threshold:
            print('- ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! ')
            print('u = ', u)
            print('U[n+1] = ', U[n+1])
            print('First if statement')


        if u == U[n+1]:
            print('- ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! - ! ')
            print('u = ', u)
            print('U[n+1] = ', U[n+1])
            print('Second if statement')
            return n

        # Binary search
        low = p
        high = n + 1
        mid = int((low + high)/2)

        while (u < (U[mid]) or u >= (U[mid+1])):
            #print("----------------------------------")
            #print('u = ', u)
            #print('U[mid] = ', U[mid])
            #print('U[mid+1] = ', U[mid+1])
            #print('low = ', low)
            #print('high = ', high)
            #print('mid = ', mid)
            #print('u < U[mid] = ', u < U[mid])
            #print('u >= U[mid+1] = ', u >= U[mid+1])
            #print("- - - -")
            if u < U[mid]:
                high = mid
            else:
                low = mid
            mid = int(np.floor((low + high)/2))
            #print('U[mid] = ', U[mid])
            #print('U[mid+1] = ', U[mid+1])
            #print('low = ', low)
            #print('high = ', high)
            #print('mid = ', mid)
            #print('u < U[mid] = ', u < U[mid])
            #print('u >= U[mid+1] = ', u >= U[mid+1])
            #Pause
            #input("Press Enter to continue...")
        return mid
    else:
        threshold = 1e-5
        for i in range(0,U.size-1):
            #print('----------------------------------')
            #print('U[i]-threshold = ', U[i]-threshold)
            #print('U[i+1]+threshold = ', U[i+1]+threshold)
            #print('u = ', u)
            #print('u > U[i]-threshold = ', u > U[i]-threshold)
            #print('u <= U[i+1]+threshold = ', u <= U[i+1]+threshold)
            if u > U[i]-threshold and u <= U[i+1]+threshold:
                #print(' i = ', i)
                return i

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
        #print('left[j] = ', left[j])
        #print('i = ', i)
        #print('j = ', j)
        #print('i+1-j = ', i+1-j)
        #print('U[i+1-j] = ', U[i+1-j])
        #print('u = ', u)
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
    # Algorithm A4.1 from 'The NURBS Book'
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
#P = np.array([(1.58708, 0.196605),(3.05134, 0.334602),(4.32673, 0.354718),(5.5079 ,0.451016),(6.40793, 0.498087),(7.19846, 0.439246),(7.49318, 0.44306),(9.50855, 0.731002),(10.7131, 1.03833),(11.6019, 1.09408),(12.8493, 1.48369),(13.953, 1.9465),(15.3118, 2.81175),(15.9799, 3.79806),(16.5821, 4.8731),(16.8734, 6.15095),(17.2845, 7.64105),(17.1563, 9.2268),(17.1664, 10.566),(17.1057, 12.1092),(17.1393, 13.1508),(16.5204, 16.0782),(15.696, 17.0725),(14.7033, 18.6581),(13.6278, 19.4366),(12.3093, 20.3027),(10.7861, 20.9667),(9.8253, 21.4885),(7.04258, 21.7556),(6.15898, 21.7439),(4.70433, 21.8898),(3.86209, 21.9412),(2.74298, 22.3858),(1.6161, 23.3269),(0.931441, 23.9076),(0.198518, 24.5167),(-0.613045, 25.2146),(-1.48553, 25.5106),(-2.50185, 25.9521),(-3.68042, 25.8867),(-4.37892, 25.6825),(-5.62569, 25.009),(-6.77287, 23.8039),(-7.42617, 23.0727),(-8.18589, 22.2181),(-8.95121, 21.4155),(-9.85661, 20.6733),(-11.7417, 19.8699),(-12.9495, 20.0955),(-13.7765, 20.2894),(-14.8553, 20.9888),(-14.9925, 21.3058),(-15.8809, 21.7201),(-16.8964, 22.4726),(-18.1459, 23.0303),(-19.6929, 23.2201),(-21.6914, 23.3649),(-23.0661, 23.0005),(-24.9952, 22.547),(-26.2839, 21.6748),(-27.614, 20.8144),(-30.352, 18.9578),(-31.284, 18.0183),(-32.4286, 16.9183),(-34.0388, 14.3546),(-35.4079, 11.4908),(-35.9148, 9.74627),(-36.3602, 8.23571),(-37.2716, 5.36413),(-37.4675, 4.04943),(-37.7236, 2.72449),(-37.8933, 0.708806),(-37.7319, -1.01034),(-37.6355, -2.82151),(-37.5889, -4.27061),(-37.2529, -6.36517),(-36.7624, -8.10747),(-35.9371, -9.51755),(-35.0562, -10.5404),(-33.7657, -11.7274),(-32.304, -14.1412),(-30.86, -12.5166),(-30.8696, -14.3115),(-30.4804, -13.4108),(-29.5355, -13.8028),(-27.9378, -13.9544),(-26.8466, -13.844),(-24.9096, -13.3396),(-23.8324, -12.8998),(-23.0544, -12.1269),(-22.3988, -11.4572),(-22.0327, -10.7583),(-21.5626, -8.76889),(-21.3556, -7.8387),(-21.9449, -6.45562),(-22.7156, -4.85865),(-23.1567, -3.67757),(-24.2726, -0.652197),(-24.538, 0.429136),(-24.7079, 2.0639),(-24.8392, 3.26428),(-24.857, 4.35029),(-24.8176, 5.44256),(-24.7781, 6.54035),(-24.3795, 7.52234),(-24.0658, 8.5894),(-23.4675, 9.67208),(-22.743, 10.7701),(-21.8308, 11.6643),(-20.4964, 12.4293),(-19.8862, 12.9206),(-17.9901, 13.0725),(-16.731, 12.8293),(-15.8134, 12.3757),(-14.6179, 11.643),(-13.4003, 10.5307),(-14.2318, 11.0509),(-13.2849, 10.1801),(-12.4534, 9.65996),(-11.6707, 8.61251),(-10.4666, 7.32961),(-9.56441, 6.2947),(-8.08557, 4.78137),(-6.83681, 3.88471),(-5.37015, 2.79938),(-4.25354, 1.93765),(-2.93201, 1.24044),(-1.386, 0.431934),(-0.132915, 0.125074)]) #                <-- Control points
#P = np.array([[0,1], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], [8,0], [9,0], [10,0]])
#P = np.array([[0,0], [1,0], [2,0], [2,1], [2,2], [1,2], [0,2], [0,1], [0,0], [1,0]])


p = 2#                                                 <-- Degree of the curve
# We want to close the curve, so we add 'degree' number of points to the end of P that are equal to the first 'degree' points in P
#for i in range(0,p):
#   P = np.append(P, [P[i]], axis=0)

n = P.shape[0] - 1
if isBspline:
    w = np.ones((n+1))
else:
    w = np.array([1, 4, 1, 1, 1]) #             <-- Weights (depends on isBspline)
# Auto determine the knots
autoDeterminKnots = False #                         <-- Auto determine the knots
autoDeterminKnotsCorrect = True
clampedStart = True
clampedEnd = True

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
r = (n+1) + p
# We want to clamp the end knots, so the first p+1 knots are equal to 0 and
# the last p+1 knots are equal to 1 
UStart = np.zeros((p+1))
UEnd = np.ones((p+1))
# UMid is of size n - p
#TODO: U is not correct, currently the mid is Umid \in (0,1) but it should be that Umid is just a continuation of Ustart and Uend
#EX: Current U =  [0, 0, 0, 0.25, 0.5, 0.75, 1, 1, 1]
#    Correct U = [0, 0, 0, 0.375, 0.5, 0.625, 1, 1, 1]
if autoDeterminKnots:
    UMid = np.linspace(0,1,n-p+2)
    UMid = np.delete(UMid, 0)
    lastUMidIndex = UMid.shape[0]-1
    UMid = np.delete(UMid, lastUMidIndex)
    U = np.concatenate((UStart, UMid, UEnd))
elif autoDeterminKnotsCorrect:
    U = np.linspace(0,1,r+1)
    if clampedStart:
        U[0:p+1] = 0

    if clampedEnd:
        U[r-p:] = 1
else:
    U = np.array([0, 0.091, 0.182, 0.273, 0.364, 0.455, 0.545 ,0.636, 0.727, 1, 1, 1])
#U = np.linspace(0, 1, r + 1)
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

distanceBetweenPoints = 0
numberOfControlPoints = n+1
pointsPerMeter_ = 1

for i in range(1,numberOfControlPoints):
    firstPower = np.power(P[i,0] - P[i-1,0], 2)
    secondPower = np.power(P[i,1] - P[i-1,1], 2)
    distanceBetweenPoints += np.sqrt(firstPower + secondPower)

totalPoints = pointsPerMeter_ * distanceBetweenPoints
totalPoints = int(totalPoints)
print('Total points = ', totalPoints)

#u = np.linspace(0,max(U),totalPoints)
print('U = ', U)
print('m-p = ', m-p)
print('m-p-1 = ', m-p-1)
sizeOfU = U.shape[0]
print('Size of U = ', sizeOfU)
print('p - 1 = ', p-1)
print('U[-p-1] = ', U[-p-1])
print('U[sizeOfU-p] = ', U[sizeOfU-p])
print('U[sizeOfU-p-1] = ', U[sizeOfU-p-1])
totalPoints = 100
u = np.linspace(U[p], U[-(p+1)], totalPoints)
C = np.zeros((u.shape[0],P.shape[1]))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
print('Calculating curve points')
t = time.time()
for inx in range(0,u.shape[0]):
    C[inx,:] = CurvePoint(n,p,U,Pw,u[inx])

#print('Time elapsed = ', time.time() - t)

plt.figure()
if isBspline:
    plt.title('B-spline curve')
else:
    plt.title('Rational B-spline curve')

plt.plot(P[:,0], P[:,1], 'o', label='Control points')
plt.plot(C[:,0], C[:,1], 'o--', label='Curve point of degree ' + str(p), linewidth=2)
plt.legend()
plt.show()

