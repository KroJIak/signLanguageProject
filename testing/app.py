import os
from copy import copy

from testing.modules.const import ConstPlenty
from testing.modules.database.worker import dbDictWorker, dbGestureWorker
from utils.devices import Camera
from utils.hands.detector import HandDetector
from utils.objects import Position, Vector
from utils.funcs import getLengthVector, getAngleBetweenVectors, getRotatedVectorAroundY

import cv2

const = ConstPlenty()

detHands = HandDetector(detectionCon=0.6, minTrackCon=0.6)
dbDictionaries = dbDictWorker()

def getNeedHandByType(realHands, masterHand):
    for hand in realHands:
        if hand.typeHand == masterHand.typeHand: return hand
    return None

# ЭЩКЕРЕ

def getRiggedMasterHand(masterHand, realHand):
    riggedMasterHand = copy(masterHand)
    resultBones = []
    for id, realHand in enumerate(realHand.bones):
        newBone = copy(masterHand.bones[id])
        newBone.prod(getLengthVector(realHand))
        resultBones.append(newBone)
    riggedMasterHand.bones = resultBones
    return riggedMasterHand

def getStartPositionOfBone(masterBones, startPoint, parentId, resultPosition):
    if parentId == -1:
        resultPosition.add(startPoint)
        return resultPosition
    resultPosition.add(masterBones[parentId])
    nextParentId = const.hands.bones.parentPoints[parentId]
    return getStartPositionOfBone(masterBones, startPoint, nextParentId, resultPosition)

def getVerticalRotatedMasterHand(hand, angle):
    rotatedMasterHand = copy(hand)
    resultBones = []
    for bone in hand.bones:
        resultBones.append(getRotatedVectorAroundY(bone, angle))
    rotatedMasterHand.bones = resultBones
    return rotatedMasterHand

def drawPoints(img, hands):
    for hand in hands:
        for point in hand.lmList:
            cv2.circle(img, (int(point.x), int(point.y)), 3, (0, 0, 255), -1)

def drawLines(img, hand):
    startPoint = hand.lmList[0]
    for bone in hand.bones:
        startPos = getStartPositionOfBone(hand.bones, startPoint, bone.parentId, Position(0, 0, 0))
        endPos = copy(startPos)
        endPos.add(bone)
        cv2.line(img, (int(startPos.x), int(startPos.y)), (int(endPos.x), int(endPos.y)), (255, 0, 0), 3)

def drawMasterLines(img, startPoint, masterHand):
    for id, bone in enumerate(masterHand.bones):
        startPos = getStartPositionOfBone(masterHand.bones, startPoint, bone.parentId, Position(0, 0, 0))
        endPos = copy(startPos)
        endPos.add(bone)
        cv2.line(img, (int(startPos.x), int(startPos.y)), (int(endPos.x), int(endPos.y)), (255, 255, 255), 3)

def drawDirectionVector(img, hand):
    directionVector = Vector(0, 0, 0)
    for id in const.hands.palm.centerBones:
        bone = hand.bones[id]
        directionVector.add(bone)
    startPos = hand.lmList[0]
    endPos = copy(startPos)
    endPos.add(directionVector)
    cv2.arrowedLine(img, (int(startPos.x), int(startPos.y)), (int(endPos.x), int(endPos.y)), (255, 30, 0), 3)

def drawNormalVector(img, hand):
    centerPalmPoints = [hand.lmList[id] for id in const.hands.palm.centerPoints]
    averageX = sum([point.x for point in centerPalmPoints]) / len(centerPalmPoints)
    averageY = sum([point.y for point in centerPalmPoints]) / len(centerPalmPoints)
    averageZ = sum([point.z for point in centerPalmPoints]) / len(centerPalmPoints)
    normalVector = hand.normalVector
    normalVector.prod(100)
    startPos = Position(averageX, averageY, averageZ)
    endPos = copy(startPos)
    endPos.add(normalVector)
    cv2.arrowedLine(img, (int(startPos.x), int(startPos.y)), (int(endPos.x), int(endPos.y)), (0, 220, 0), 3)

def main():
    dictionaryPath = dbDictionaries.getDictionaryPath('Дактиль')
    dbGesture = dbGestureWorker(dictionaryPath)
    gesture = dbGesture.getGesture('Н')

    cam = Camera(const.camera.index, flip=True)
    while True:
        img = cam.read()

        realHands = detHands.findHands(img)
        for masterHand in gesture.hands:
            needRealHand = getNeedHandByType(realHands, masterHand)
            if needRealHand is None: continue
            riggedMasterHand = getRiggedMasterHand(masterHand, needRealHand)
            masterNormalVector, realNormalVector = riggedMasterHand.normalVector, needRealHand.normalVector
            masterNormalVector.y, realNormalVector.y = 0, 0
            angleBetweenNormals = getAngleBetweenVectors(masterNormalVector, realNormalVector, useAbs=False)
            rotatedMasterHand = getVerticalRotatedMasterHand(riggedMasterHand, angleBetweenNormals)

            drawMasterLines(img, needRealHand.lmList[0], rotatedMasterHand)
            drawLines(img, needRealHand)
            drawNormalVector(img, needRealHand)
        if realHands: drawPoints(img, realHands)

        cv2.imshow('Image', img)
        if cv2.waitKey(1) == 27: break
    cv2.destroyAllWindows()
    cam.release()

if __name__ == '__main__':
    main()