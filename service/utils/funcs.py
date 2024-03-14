from math import sqrt, pi, acos
import numpy as np
from service.utils.const import Position

def getAngleBetweenLines(line1, line2, thirdDim=False):
    startPosLine1, endPosLine1 = line1
    startPosLine2, endPosLine2 = line2
    if thirdDim: dims = ['x', 'y', 'z']
    else: dims = ['x', 'y']
    vector1 = {axis: (endPosLine1[axis] - startPosLine1[axis]) for axis in dims}
    vector2 = {axis: (endPosLine2[axis] - startPosLine2[axis]) for axis in dims}
    scalarProduct = np.dot(list(vector1.values()), list(vector2.values()))
    lengthVector1 = sqrt(vector1['x'] ** 2 + vector1['y'] ** 2 + (vector1['z'] ** 2 if thirdDim else 0))
    lengthVector2 = sqrt(vector2['x'] ** 2 + vector2['y'] ** 2 + (vector2['z'] ** 2 if thirdDim else 0))
    lengthsProduct = lengthVector1 * lengthVector2
    if lengthsProduct == 0: return pi
    angle = acos(scalarProduct / lengthsProduct)
    return angle

def getDistanceBetweenPoints(point1, point2, thirdDim=False):
    if thirdDim: vector = {axis: (point1[axis] - point2[axis]) for axis in ['x', 'y', 'z']}
    else: vector = {axis: (point1[axis] - point2[axis]) for axis in ['x', 'y']}
    lengthVector = sqrt(vector['x'] ** 2 + vector['y'] ** 2 + vector['z'] if thirdDim else 0)
    return lengthVector

def convertPosTo2D(pos):
    resPos = Position(x=int(pos['x']), y=int(pos['y']))
    return resPos
