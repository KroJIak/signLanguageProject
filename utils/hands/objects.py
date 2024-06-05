from typing import List

from utils.objects import Vector

class BoneVector(Vector):
    def __init__(self, x: float, y: float, z: float, id: int, parentId: int):
        super().__init__(x, y, z)
        self.id = id
        self.parentId = parentId

    def __str__(self):
        return f'[BoneVector] id: {self.id} parentId: {self.parentId} x: {self.x} y: {self.y} z: {self.z}'

class Hand:
    def __init__(self, typeHand: str, lmList: tuple = None, bones: tuple = None, useFace=False, linkedPoints: tuple = None):
        self.typeHand = typeHand
        if lmList is None: self.lmList = []
        else: self.lmList = lmList
        if bones is None: self.bones = []
        else: self.bones = bones
        self.useFace = useFace
        if linkedPoints is None: self.linkedPoints = []
        else: self.linkedPoints = linkedPoints

    def __str__(self):
        return f'[Hand] typeHand: {self.typeHand} lmList: {self.lmList} bones: {self.bones} useFace: {self.useFace} linkedPoints: {self.linkedPoints}'

class Gesture:
    def __init__(self, name: str, hands: List[Hand]):
        self.name = name
        self.hands = hands

    def __str__(self):
        return f'[Gesture] name: {self.name} countHands {len(self.hands)}'