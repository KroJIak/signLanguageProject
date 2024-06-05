
from service.modules.const import ConstPlenty, WebPosition, WebPoint, WebLine
from service.modules.funcs import *

const = ConstPlenty()

def getPercentOfVectorSimilarity(vectorRealHand, vectorMasterHand):
    angle = getAngleBetweenVectors(vectorRealHand, vectorMasterHand)
    anglePercent = (math.pi - angle) / math.pi
    return anglePercent

def getNeedHandByType(realHands, masterHand):
    for hand in realHands:
        if hand.typeHand == masterHand.typeHand: return hand
    return None

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

def getColorLine(linePercent, previousColor, aplha=0.6):
    R = 255
    G = min(round(255 * linePercent), previousColor[1])
    B = min(round(255 * linePercent), previousColor[2])
    resultColor = (R, G, B, aplha)
    return resultColor

def getResultWebLine(start, end, color, thickness=3):
    resultLine = WebLine(start=start,
                         end=end,
                         color=color,
                         thickness=thickness)
    return resultLine

def getResultLineHands(realHands, realFaces, masterGesture):
    resultLines = []
    for masterHand in masterGesture.hands:
        needRealHand = getNeedHandByType(realHands, masterHand)
        if needRealHand is None: continue
        handLines = []
        faceDistancePercent = getFaceDistancePercent(needRealHand, masterHand, realFaces)
        bonesRealHand = needRealHand.bones
        bonesMasterHand = masterHand.bones
        for index in range(len(bonesMasterHand)):
            linePercent = getPercentOfVectorSimilarity(bonesRealHand[index], bonesMasterHand[index]) * faceDistancePercent
            parentPoint = const.hands.bones.parentPoints[bonesRealHand[index].id]
            previousColor = handLines[parentPoint].color if parentPoint != -1 else (255, 255, 255, 1)
            colorLine = getColorLine(linePercent, previousColor)
            startPointId, endPointId = bonesRealHand[index].id + 1, bonesRealHand[index].parentId + 1
            startPoint, endPoint = needRealHand.lmList[startPointId], needRealHand.lmList[endPointId]
            startWebPosition = WebPosition(x=int(startPoint.x), y=int(startPoint.y))
            endWebPosition = WebPosition(x=int(endPoint.x), y=int(endPoint.y))
            resLine = getResultWebLine(startWebPosition, endWebPosition, colorLine)
            handLines.append(resLine)
        resultLines += handLines
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