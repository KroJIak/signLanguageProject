
import math

def getDistanceBetweenPoints(pnt1, pnt2) -> float:
    dx = pnt1.x - pnt2.x
    dy = pnt1.y - pnt2.y
    dz = pnt1.z - pnt2.z
    return (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

def getLengthVector(vec) -> float:
    return (vec.x ** 2 + vec.y ** 2 + vec.z ** 2) ** 0.5

def getScalarProduct(vec1, vec2) -> float:
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z

def getAngleBetweenVectors(vector1, vector2) -> float:
    scalarProduct = getScalarProduct(vector1, vector2)
    lengthVector1 = getLengthVector(vector1)
    lengthVector2 = getLengthVector(vector2)
    lengthsProduct = lengthVector1 * lengthVector2
    if lengthsProduct == 0: return math.pi
    angle = math.acos(scalarProduct / lengthsProduct)
    return angle