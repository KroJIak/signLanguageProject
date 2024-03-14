import mediapipe as mp
import multiprocessing
from pydantic import BaseModel
from service.utils.const import ConstPlenty, Position, Point, Line
from service.utils.funcs import *
import cv2

const = ConstPlenty()

def flipHand(side): return const.hands.right if side == const.hands.left else const.hands.left

class Hand(BaseModel):
    lmList: list
    type: str

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)


    def getResults(self, imgRGB):
        self.results = self.hands.process(imgRGB)

    def findHands(self, img, flip=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        processFinding = multiprocessing.Process(self.getResults(imgRGB))
        while processFinding.is_alive(): pass
        self.height, self.width = img.shape[:2]
        allHands = []
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                lmList = []
                for lm in handLms.landmark:
                    px, py, pz = lm.x * self.width, lm.y * self.height, lm.z * self.width
                    lmList.append(dict(x=px, y=py, z=pz))
                typeHand = handType.classification[0].label.lower()
                if flip: typeHand = flipHand(typeHand)
                allHands.append(Hand(lmList=lmList, type=typeHand))
        return allHands

def getPercentOfSimilarityLines(lineRealHand, lineMasterHand):
    angle = getAngleBetweenLines(lineRealHand, lineMasterHand, thirdDim=True)
    anglePercent = (pi - angle) / pi
    return anglePercent

def getNeedHandByType(realHands, typeHand):
    for hand in realHands:
        if hand.type == typeHand: return hand
    return None

def getFaceDistancePercent(lmListRealHand, realFaces, masterGesture):
    if not masterGesture['useFace']: return 1
    if not realFaces: return 0
    face = realFaces[-1]
    lmListRealFace = face.lmList
    averageDistancePoints = []
    for pointHand, pointFace, needDistance in masterGesture['linkedPointsWithFace']:
        distancePoints = getDistanceBetweenPoints(lmListRealHand[pointHand], lmListRealFace[pointFace], thirdDim=True)
        distanceRatio = needDistance / distancePoints if distancePoints > 0 else 1
        averageDistancePoints.append(min(1, distanceRatio))
    distancePercent = sum(averageDistancePoints) / len(averageDistancePoints)
    return distancePercent

def getColorLine(linePercent, previousColor, aplha=0.6):
    R = 255
    G = min(round(255 * linePercent), previousColor[1])
    B = min(round(255 * linePercent), previousColor[2])
    resultColor = (R, G, B, aplha)
    return resultColor

def getResultLine(start, end, color, thickness=3):
    resultLine = Line(start=start,
                      end=end,
                      color=color,
                      thickness=thickness)
    return resultLine

def getResultLineHands(realHands, realFaces, masterGesture):
    resultLines = []
    masterHands = masterGesture['hands']
    for typeHand in masterHands:
        needRealHand = getNeedHandByType(realHands, typeHand)
        if not needRealHand: continue
        tempPos = Position(x=0, y=0)
        handLines = [getResultLine(tempPos, tempPos, (255, 255, 255, 1))]
        lmListRealHand = needRealHand.lmList
        lmListMasterHand = masterHands[typeHand]['lmList']
        distancePercent = getFaceDistancePercent(lmListRealHand, realFaces, masterGesture)
        for point in range(1, 21):
            lineRealHand = (lmListRealHand[const.hands.parentPoints[point]], lmListRealHand[point])
            lineMasterHand = (lmListMasterHand[const.hands.parentPoints[point]], lmListMasterHand[point])
            linePercent = getPercentOfSimilarityLines(lineRealHand, lineMasterHand) * distancePercent
            startPos = convertPosTo2D(lineRealHand[0])
            endPos = convertPosTo2D(lineRealHand[1])
            previousColor = handLines[const.hands.parentPoints[point]].color
            colorLine = getColorLine(linePercent, previousColor)
            resLine = getResultLine(startPos, endPos, colorLine)
            handLines.append(resLine)
        resultLines += handLines
    return resultLines

def getPointsFromHands(hands, color=(40, 240, 40, 0.3), radius=3):
    if not hands: return []
    hands = hands[-2:]
    points = []
    for hand in hands:
        for realPos in hand.lmList:
            screenPos = Position(x=int(realPos['x']), y=int(realPos['y']))
            points.append(Point(pos=screenPos, color=color, radius=radius))
    return points