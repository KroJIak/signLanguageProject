from math import sqrt, acos, pi
import mediapipe as mp
import multiprocessing
from copy import copy
import numpy as np
import cv2


PARENT_POINTS = [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19]
FLIP_HAND_DICT = {
    'Right': 'Left',
    'Left': 'Right'
}

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

    def findHands(self, img, flipType=True):
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

                typeHand = handType.classification[0].label
                scoreHand = handType.classification[0].score
                if flipType: typeHand = FLIP_HAND_DICT[typeHand]
                allHands.append({
                    'lmList': lmList,
                    'type': typeHand,
                    'score': scoreHand
                })
        return allHands

    def findWorldHands(self, img, flipType=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        processFinding = multiprocessing.Process(self.getResults(imgRGB))
        while processFinding.is_alive(): pass
        self.height, self.width = img.shape[:2]
        allHands = []
        if self.results.multi_hand_world_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_world_landmarks):
                lmList = []
                for lm in handLms.landmark:
                    multip = 2000
                    px, py, pz = self.width // 2 + lm.x * multip, self.height // 2 + lm.y * multip, self.width // 2 + lm.z * multip
                    lmList.append(dict(x=px, y=py, z=pz))

                typeHand = handType.classification[0].label
                scoreHand = handType.classification[0].score
                if flipType: typeHand = FLIP_HAND_DICT[typeHand]
                allHands.append({
                    'lmList': lmList,
                    'type': typeHand,
                    'score': scoreHand
                })
        return allHands

    def getGestureNameByImg(self, img):
        return ('assets', 'А')

class drawHandWorker():
    def drawLine(self, img, posPoints, prePoint, curPoint, color, thickness):
        resultImg = copy(img)
        pos1 = dict(x=int(posPoints[prePoint]['x']), y=int(posPoints[prePoint]['y']))
        pos2 = dict(x=int(posPoints[curPoint]['x']), y=int(posPoints[curPoint]['y']))
        cv2.line(resultImg, (pos1['x'], pos1['y']), (pos2['x'], pos2['y']), color, thickness)
        return resultImg

    def drawLinesOnImgFromPoints(self, img, lmList, colorLines, thickness):
        resultImg = copy(img)
        for point in range(1, 21):
            resultImg = self.drawLine(resultImg, lmList, PARENT_POINTS[point], point, colorLines[point], thickness)
        return resultImg

    def getColorLinesHand(self, resultHands, lineHandsPercent):
        colorLinesHand = {
            'Right': [[255, 255, 255, 255]] * 21,
            'Left': [[255, 255, 255, 255]] * 21
        }
        for typeHand in resultHands:
            handPercent = lineHandsPercent[typeHand]
            for point in range(1, 21):
                colorLinesHand[typeHand][point] = [
                min(round(255 * handPercent[point]), colorLinesHand[typeHand][PARENT_POINTS[point]][0]),
                min(round(255 * handPercent[point]), colorLinesHand[typeHand][PARENT_POINTS[point]][1]),
                255,
                255]
        return colorLinesHand


class globalHandWorker():
    def getResultHands(self, realHands):
        if not realHands: return []
        resultHands = {hand['type']: {'lmList': hand['lmList'],
                                   'score': hand['score']} for hand in realHands}
        return resultHands

    def getOnlyMainHands(self, hands):
        if hands is None: return None
        newHands = {}
        for hand in hands:
            newHands[hand['type']] = {
                'lmList': hand['lmList'],
                'score': hand['score']
            }
        return newHands

    def onlyMainHands2LmList(self, hands):
        lmList = [hands[typeHand]['lmList'] for typeHand in hands]
        return lmList

    def getAngleBetweenLines(self, line1, line2):
        startPosLine1, endPosLine1 = line1
        startPosLine2, endPosLine2 = line2
        vector1 = {axis: (endPosLine1[axis] - startPosLine1[axis]) for axis in ['x', 'y', 'z']}
        vector2 = {axis: (endPosLine2[axis] - startPosLine2[axis]) for axis in ['x', 'y', 'z']}
        scalarProduct = np.dot(list(vector1.values()), list(vector2.values()))
        lengthVector1 = sqrt(vector1['x']**2 + vector1['y']**2 + vector1['z']**2)
        lengthVector2 = sqrt(vector2['x']**2 + vector2['y']**2 + vector2['z']**2)
        lengthsProduct = lengthVector1 * lengthVector2
        if lengthsProduct == 0: return pi
        angle = acos(scalarProduct / lengthsProduct)
        return angle

    def getDistanceBetweenPoints2Dimg(self, point1, point2):
        vector = {axis: (point1[axis] - point2[axis]) for axis in ['x', 'y']}
        lengthVector = sqrt(vector['x'] ** 2 + vector['y'] ** 2)
        return lengthVector

    def getPercentLinesHandSimilarity(self, lmListFullHand, lmListRealHand, numPoint):
        angle = self.getAngleBetweenLines((lmListRealHand[PARENT_POINTS[numPoint]], lmListRealHand[numPoint]),
                                                (lmListFullHand[PARENT_POINTS[numPoint]], lmListFullHand[numPoint]))
        anglePercent = (pi - angle) / pi
        return anglePercent

    def getLineHandsPercent(self, resultHands, fullGesture, resultFace=None):
        fullHands = fullGesture['hands']
        lineHandsPercent = {'Right': [1] + [0] * 20, 'Left': [1] + [0] * 20}
        for typeHand in fullHands:
            if typeHand not in resultHands: continue
            lmListRealHand = resultHands[typeHand]['lmList']
            lmListFullHand = fullHands[typeHand]['lmList']
            for point in range(1, 21):
                lineHandsPercent[typeHand][point] = self.getPercentLinesHandSimilarity(lmListFullHand,
                                                                                       lmListRealHand, point)
            if fullGesture['useFace']:
                if resultFace:
                    averageDistancePoints = []
                    for pointHand, pointFace, needDistance in fullGesture['linkedPointsWithFace']:
                        distancePoints = self.getDistanceBetweenPoints2Dimg(
                            resultHands[typeHand]['lmList'][pointHand],
                            resultFace['lmList'][pointFace])
                        distanceRatio = needDistance / distancePoints if distancePoints > 0 else 1
                        averageDistancePoints.append(min(1, distanceRatio))
                    distancePercent = sum(averageDistancePoints) / len(averageDistancePoints)
                else:
                    distancePercent = 0
                lineHandsPercent[typeHand] = np.dot(lineHandsPercent[typeHand], distancePercent)
        return lineHandsPercent

    def getResultPercent(self, hands, fullGesture, face, indexCount):
        lineHandsPercent = self.getLineHandsPercent(hands, fullGesture, face)
        if indexCount == 0:
            resultPercent = [sum(lineHandsPercent[typeHand][1:]) / (len(lineHandsPercent[typeHand]) - 1)
                             for typeHand in lineHandsPercent if typeHand in fullGesture['hands']]
            resultPercent = sum(resultPercent) / 2
        elif indexCount == 1:
            typeHand = list(hands.keys())[0]
            resultPercent = sum(lineHandsPercent[typeHand][1:]) / (len(lineHandsPercent[typeHand]) - 1)
        return resultPercent, lineHandsPercent

    def getMaxPossibleGesture(self, hands, face, dbData, oldGestureData=None):
        if oldGestureData:
            fullGesture = dbData[oldGestureData['type']]['gestures'][oldGestureData['name']]
            gestureInfo = dbData[oldGestureData['type']]['info']
            for ind, category in enumerate(gestureInfo):
                if oldGestureData['name'] in gestureInfo[category]:
                    indexCount = ind
                    break
            resultPercent, lineHandsPercent = self.getResultPercent(hands, fullGesture, face, indexCount)
            if resultPercent >= oldGestureData['percent']:
                return oldGestureData['type'], oldGestureData['name'], resultPercent, lineHandsPercent
        maxPercentList = self.getZeroLineHandPercent()
        maxGestureName = None
        maxGestureType = None
        maxPercent = 0
        for gestureType in dbData:
            if not len(dbData[gestureType]): continue
            gestureInfo = dbData[gestureType]['info']
            for ind, category in enumerate(gestureInfo):
                countHandList = gestureInfo[category]
                for gestureName in countHandList:
                    fullGesture = dbData[gestureType]['gestures'][gestureName]
                    resultPercent, lineHandsPercent = self.getResultPercent(hands, fullGesture, face, ind)
                    if resultPercent > maxPercent:
                        maxPercent = resultPercent
                        maxGestureType = gestureType
                        maxGestureName = gestureName
                        maxPercentList = lineHandsPercent.copy()
        return maxGestureType, maxGestureName, maxPercent, maxPercentList

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FPS, 30)
    detector = handDetector(detectionCon=0.8, maxHands=4)
    while cv2.waitKey(1) != 27:
        success, img = cap.read()
        height, width = img.shape[:2]
        zeroImg = np.zeros((height, width, 3), dtype=np.uint8)
        hands = detector.findHands(img)
        if success:
            if hands:
                print(hands)
                for hand in hands:
                    zeroImg = drawHand.drawLinesOnImgFromPoints(zeroImg, hand["lmList"], [(0, 210, 0)] * 21, 4)
                cv2.imshow("Image-lines", zeroImg)
            cv2.imshow("Image", img)


if __name__ == "__main__":
    handWorker = globalHandWorker()
    drawHand = drawHandWorker()
    main()
