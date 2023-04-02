import numpy as np

from nurbsAlgorithms import CurvePoint

class NURBS:

    _totalNumberOfPoints = 0
    _degree = 0
    _typOfCurve = ''
    _controlPoints = np.empty((0,0))

    def __init__(self, totalNumberOfPoints: int):
        self._totalNumberOfPoints = totalNumberOfPoints
        print('NURBS!')
    
    # WARNING: 2d Bezier curve
    def constructBezier(self, controlPoints: np.ndarray):
        self._controlPoints = controlPoints
        self._typOfCurve = 'Bezier'
        numberOfControlPoints = controlPoints.shape[0]
        numberOfDimensions = controlPoints.shape[1]
        n = numberOfControlPoints - 1

        # The degree of the Bezier curve is numberOfControlPoints - 1
        degree = n
        self._degree = degree

        # A Bezier curve starts and ends at the first and last control point
        # In other words, it is clamped at the start and end
        clampedStart = True
        clampedEnd = True

        numberOfKnots = n + degree + 2
        r = numberOfKnots - 1

        # For a Bezier curve, the knot vector is [0, 0, ..., 0, 1, 1, ..., 1]
        knots = np.linspace(0,1,r+1)
        if clampedStart:
            knots[0:degree+1] = 0
        if clampedEnd:
            knots[r-degree:] = 1
        numberOfKnots = knots.shape[0]
        m = numberOfKnots - 1

        # For a Bezier curve, the weights are all 1
        weights = np.ones(numberOfControlPoints)

        controlPointsWithWeights = np.zeros((numberOfControlPoints,
                                             numberOfDimensions+1))
        for idx, point in enumerate(controlPoints):
            controlPointsWithWeights[idx,0] = point[0] * weights[idx]
            controlPointsWithWeights[idx,1] = point[1] * weights[idx]
            controlPointsWithWeights[idx,2] = weights[idx]


        timeSteps = np.linspace(knots[degree], knots[-(degree+1)], self._totalNumberOfPoints)
        curvePointsMatrix = np.zeros((self._totalNumberOfPoints, numberOfDimensions))

        for inx, u in enumerate(timeSteps):
            curvePointsMatrix[inx,:] = CurvePoint(n, degree, knots, 
                                             controlPointsWithWeights, u)

        return curvePointsMatrix

    #TODO: Should maybe be in a separate class
    def findClosestPoint(self, mousePoint: np.ndarray):
        controlPoints = self._controlPoints

        cloasestPoint = np.linalg.norm(mousePoint - controlPoints[0])
        cloasestPointIdx = 0
        for idx, point in enumerate(controlPoints):
            tempCloasestPoint = np.linalg.norm(mousePoint - point)
            if tempCloasestPoint < cloasestPoint:
                cloasestPoint = tempCloasestPoint
                cloasestPointIdx = idx

        return cloasestPointIdx

    # - - - - - Getters - - - - -
    def getDegree(self):
        return self._degree

    def getTypOfCurve(self):
        return self._typOfCurve

    # - - - - - Setters - - - - -

    

