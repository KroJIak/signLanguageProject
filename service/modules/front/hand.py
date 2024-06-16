
import math
from copy import copy

from service.modules.const import ConstPlenty
from service.modules.objects import WebPosition, WebPoint, WebLine
from utils.funcs import getAngleBetweenVectors, getDistanceBetweenPoints, getLengthVector, getRotatedVectorAroundY
from utils.objects import Position

const = ConstPlenty()

def getNeedHandByType(realHands, masterHand):
    for hand in realHands:
        if hand.typeHand == masterHand.typeHand: return hand
    return None

def getPercentOfVectorSimilarity(vectorRealHand, vectorMasterHand):
    angle = getAngleBetweenVectors(vectorRealHand, vectorMasterHand)
    anglePercent = (math.pi - angle) / math.pi
    return anglePercent

# ЭЩКЕРЕ 2x

def getFaceDistancePercent(realHand, masterHand, realFaces):
    if not masterHand.useFace: return 1
    if not realFaces: return 0
    realFace = realFaces[-1]
    averageDistancePoints = []
    for linkedPoint in masterHand.linkedPoints:
        distancePoints = getDistanceBetweenPoints(realHand.lmList[linkedPoint.handPointId],
                                                  realFace.lmList[linkedPoint.facePointId])
        distanceRatio = linkedPoint.dist / distancePoints if distancePoints > 0 else 1
        averageDistancePoints.append(min(1, distanceRatio))
    distancePercent = sum(averageDistancePoints) / len(averageDistancePoints)
    return distancePercent


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

def getColorLine(linePercent, previousColor, aplha=0.6):
    R = 255
    G = min(round(255 * linePercent), previousColor[1])
    B = min(round(255 * linePercent), previousColor[2])
    resultColor = (R, G, B, aplha)
    return resultColor

def getColorGhostLine(linePercent, maxAlpha=0.7):
    alpha = (1 - linePercent) * maxAlpha
    resultColor = (255, 255, 255, alpha)
    return resultColor

def getRotatedMasterHand(masterHand, realHand):
    riggedMasterHand = getRiggedMasterHand(masterHand, realHand)
    masterNormalVector, realNormalVector = riggedMasterHand.normalVector, realHand.normalVector
    masterNormalVector.y, realNormalVector.y = 0, 0
    angleBetweenNormals = getAngleBetweenVectors(masterNormalVector, realNormalVector, useAbs=False)
    rotatedMasterHand = getVerticalRotatedMasterHand(riggedMasterHand, angleBetweenNormals)
    return rotatedMasterHand

def getBoneCorrectPercents(realHand, masterHand):
    boneCorrectPercents = []
    for index in range(len(realHand.bones)):
        bonePercent = getPercentOfVectorSimilarity(realHand.bones[index], masterHand.bones[index])
        boneCorrectPercents.append(bonePercent)
    return boneCorrectPercents

def getWebLineByBone(hand, startPoint, bone, color, thickness):
    startPosition = getStartPositionOfBone(hand.bones, startPoint, bone.parentId, Position(0, 0, 0))
    endPosition = copy(startPosition)
    endPosition.add(bone)
    startWebPosition = WebPosition(x=int(startPosition.x), y=int(startPosition.y))
    endWebPosition = WebPosition(x=int(endPosition.x), y=int(endPosition.y))
    resultWebLine = WebLine(start=startWebPosition, end=endWebPosition, color=color, thickness=thickness)
    return resultWebLine

def getResultLineHands(realHands, realFaces, masterGesture):
    resultLines = []
    for masterHand in masterGesture.hands:
        needRealHand = getNeedHandByType(realHands, masterHand)
        if needRealHand is None: continue
        rotatedMasterHand = getRotatedMasterHand(masterHand, needRealHand)
        boneCorrectPercents = getBoneCorrectPercents(needRealHand, rotatedMasterHand)
        faceDistancePercent = getFaceDistancePercent(needRealHand, rotatedMasterHand, realFaces)

        handLines, ghostHandLines = [], []
        startPoint = needRealHand.lmList[0]
        for index, percent in enumerate(boneCorrectPercents):
            realCurrentBone = needRealHand.bones[index]
            parentPoint = const.hands.bones.parentPoints[realCurrentBone.id]
            previousColor = handLines[parentPoint].color if parentPoint != -1 else (255, 255, 255, 1)
            colorLine = getColorLine(percent * faceDistancePercent, previousColor)
            realWebLine = getWebLineByBone(needRealHand, startPoint, realCurrentBone, colorLine, 3)
            handLines.append(realWebLine)

            ghostCurrentBone = rotatedMasterHand.bones[index]
            colorGhostLine = getColorGhostLine(percent)
            ghostWebLine = getWebLineByBone(rotatedMasterHand, startPoint, ghostCurrentBone, colorGhostLine, 4)
            ghostHandLines.append(ghostWebLine)

        resultLines += handLines + ghostHandLines
    return resultLines

def getPointsFromHands(hands, color=(40, 240, 40, 0.3), radius=3):
    if not hands: return []
    hands = hands[-2:]
    points = []
    for hand in hands:
        for point in hand.lmList:
            webPosition = WebPosition(x=int(point.x), y=int(point.y))
            points.append(WebPoint(pos=webPosition, color=color, radius=radius))
    return points