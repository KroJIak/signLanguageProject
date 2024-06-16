
import numpy as np

class Position:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def add(self, anotherPos):
        self.x += anotherPos.x
        self.y += anotherPos.y
        self.z += anotherPos.z

    def prod(self, coef: float):
        self.x *= coef
        self.y *= coef
        self.z *= coef

    def __str__(self):
        return f'[Position] x: {self.x} y: {self.y} z: {self.z}'

class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def add(self, anotherVector):
        self.x += anotherVector.x
        self.y += anotherVector.y
        self.z += anotherVector.z

    def prod(self, coef: float):
        self.x *= coef
        self.y *= coef
        self.z *= coef

    def setArray(self, array):
        self.x, self.y, self.z = array

    def getArray(self):
        return np.array([self.x, self.y, self.z])

    def __str__(self):
        return f'[Vector] x: {self.x} y: {self.y} z: {self.z}'

class Point(Position):
    def __init__(self, x: float, y: float, z: float, id: int, parentId: int = -1):
        super().__init__(x, y, z)
        self.id = id
        self.parentId = parentId

    def __str__(self):
        return f'[Point] id: {self.id} parentId: {self.parentId} x: {self.x} y: {self.y} z: {self.z}'

class LinkedPoint:
    def __init__(self, handPointId: int, facePointId: int, dist: float):
        self.handPointId = handPointId
        self.facePointId = facePointId
        self.dist = dist

    def __str__(self):
        return f'[linkedPoint] handPointId: {self.handPointId} facePointId: {self.facePointId} dist: {self.dist}'
