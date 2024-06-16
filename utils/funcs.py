
from os.path import join as joinPath
from copy import copy
import math

from utils.objects import Vector

import numpy as np

def getUnitVector(vector):
    npVector = np.array([vector.x, vector.y, vector.z])
    lengthVector = np.linalg.norm(npVector)
    npUnitVector = npVector / lengthVector
    unitVector = Vector(*npUnitVector)
    return unitVector

def computeNormalVector(point1, point2, point3):
    npVector1 = np.array([point2.x - point1.x, point2.y - point1.y, point2.z - point1.z])
    npVector2 = np.array([point3.x - point1.x, point3.y - point1.y, point3.z - point1.z])
    npNormalVector = np.cross(npVector1, npVector2)
    normalVector = Vector(*npNormalVector)
    unitNormalVector = getUnitVector(normalVector)
    return unitNormalVector

def getDistanceBetweenPoints(pnt1, pnt2):
    dx = pnt1.x - pnt2.x
    dy = pnt1.y - pnt2.y
    dz = pnt1.z - pnt2.z
    return (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

def getLengthVector(vector):
    return (vector.x ** 2 + vector.y ** 2 + vector.z ** 2) ** 0.5

def getScalarProduct(vector1, vector2):
    return vector1.x * vector2.x + vector1.y * vector2.y + vector1.z * vector2.z

def getAngleBetweenVectors(vector1, vector2, useAbs=True):
    scalarProduct = getScalarProduct(vector1, vector2)
    lengthVector1 = getLengthVector(vector1)
    lengthVector2 = getLengthVector(vector2)
    lengthsProduct = lengthVector1 * lengthVector2
    if lengthsProduct == 0: return math.pi
    angle = math.acos(scalarProduct / lengthsProduct)
    if not useAbs:
        unitVector1 = getUnitVector(vector1)
        unitVector2 = getUnitVector(vector2)
        npUnitVector1 = unitVector1.getArray()
        npUnitVector2 = unitVector2.getArray()
        crossProduct = np.cross(np.array([npUnitVector1[0], 0, npUnitVector1[2]]),
                                np.array([npUnitVector2[0], 0, npUnitVector2[2]]))
        direction = np.sign(crossProduct[1])
        angle = angle if direction >= 0 else -angle
    return angle

def getRotatedVectorAroundY(vector, angle):
    rotationMatrix = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    npVector = np.array([vector.x, vector.y, vector.z])
    npRotatedVector = rotationMatrix @ npVector
    resultVector = copy(vector)
    resultVector.setArray(npRotatedVector)
    return resultVector