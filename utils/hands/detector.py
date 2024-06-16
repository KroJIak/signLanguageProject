
import time

from utils.funcs import computeNormalVector, getUnitVector
from utils.objects import Point, Vector
from utils.hands.objects import Hand, BoneVector
from utils.hands.const import ConstPlenty

import mediapipe as mp
import multiprocessing
import cv2

const = ConstPlenty()

def flipHand(side): return const.hands.right if side == const.hands.left else const.hands.left

class HandDetector:
    def __init__(self, maxHands=2, detectionCon=0.5, minTrackCon=0.5, staticImage=False, timer=0.3):
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.staticImage = staticImage
        self.timer = timer

        self.results = None
        self.mpHands = mp.solutions.hands
        self.detector = self.mpHands.Hands(static_image_mode=False, max_num_hands=self.maxHands,
                                           min_detection_confidence=self.detectionCon,
                                           min_tracking_confidence=self.minTrackCon)

    def updateResults(self, imgRGB):
        self.results = self.detector.process(imgRGB)

    def getLmList(self, handLms):
        lmList = []
        for id, lm in enumerate(handLms.landmark):
            px, py, pz = lm.x * self.width, lm.y * self.height, lm.z * self.width
            lmList.append(Point(px, py, pz, id, const.hands.lmList.parentPoints[id]))
        return lmList

    def getBoneVectors(self, lmList, useUnitBones):
        bones = []
        for point in lmList:
            if point.parentId == -1: continue
            parentPoint = lmList[point.parentId]
            dVector = Vector(point.x - parentPoint.x, point.y - parentPoint.y, point.z - parentPoint.z)
            if useUnitBones: dVector = getUnitVector(dVector)
            id = point.id - 1
            parentId = const.hands.bones.parentPoints[id]
            boneVector = BoneVector(dVector.x, dVector.y, dVector.z, id, parentId)
            bones.append(boneVector)
        return bones

    def findHands(self, img, flipType=False, useUnitBones=False):
        self.height, self.width = img.shape[:2]
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lastTime = time.time()
        while lastTime + self.timer > time.time():
            processFinding = multiprocessing.Process(self.updateResults(imgRGB))
            while processFinding.is_alive(): pass
            if not self.staticImage: break
        allHands = []
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                lmList = self.getLmList(handLms)
                bones = self.getBoneVectors(lmList, useUnitBones)
                centerPalmPoints = [lmList[id] for id in const.hands.palm.centerPoints]
                normalVector = computeNormalVector(*centerPalmPoints)
                typeHand = handType.classification[0].label.lower()
                if flipType: typeHand = flipHand(typeHand)
                allHands.append(Hand(typeHand, lmList, bones, normalVector))
        return allHands