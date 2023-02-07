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
        # TODO: Check if this is correct
        degree = n
        self._degree = degree

        #numberOfKnots = n + degree + 2
        #r = numberOfKnots - 1

        # For a Bezier curve, the knot vector is [0, 0, ..., 0, 1, 1, ..., 1]
        UStart = np.zeros(degree+1)
        UEnd = np.ones(degree+1)
        knots = np.concatenate((UStart, UEnd))
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


        timeSteps = np.linspace(0, max(knots), self._totalNumberOfPoints)
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

    

