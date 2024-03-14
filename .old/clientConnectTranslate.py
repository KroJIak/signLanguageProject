from PC.modules.handWorking import globalHandWorker, drawHandWorker
from PC.modules.faceWorking import globalFaceWorker, drawFaceWorker
from PC.modules.imageWorking import *
from db.modules.database import dbWorker
from traceback import format_exc
from threading import Thread
import numpy as np
import requests
import json
import cv2

PATH2DB = 'gestures/Дактиль.json'
db = dbWorker(PATH2DB)
handWorker = globalHandWorker()
faceWorker = globalFaceWorker()
drawHand = drawHandWorker()
drawFace = drawFaceWorker()

class outputImageWorker():
    def __init__(self):
        self.layers = {}
        self.resultHands = {}
        self.resultFace = {}
        self.countEmptyLayersHands = 0
        self.countEmptyLayersFace = 0
        self.filterPowerHands = 1
        self.filterPowerFace = 1
        self.colorLinesHand = drawHand.getDefaultColorLines()
        self.colorPointsFace = (0, 150, 0)

    def setLayer(self, name, img):
        self.layers[name] = img

    def setColorLinesHand(self, colorLinesHand):
        self.colorLinesHand = colorLinesHand

    def setLinesFromHands(self, resultHands):
        if resultHands is None: return
        self.filterPowerHands = handWorker.getFilterPower()
        self.resultHands = resultHands
        countHandsArr = [len(hands) for hands in handWorker.getHandsOldArray()]
        self.countEmptyLayersHands = countHandsArr.count(0)

    def setLinesFromFace(self, resultFace):
        if resultFace is None: return
        self.filterPowerFace = faceWorker.getFilterPower()
        self.resultFace = resultFace
        countFaceArr = [len(hands) for hands in faceWorker.getFacesOldArray()]
        self.countEmptyLayersFace = countFaceArr.count(0)

    def getResultImg(self, background, linesHandThickness=3, pointsFaceThickness=2, pointFaceRadius=1):
        resultImg = background.copy()
        for key in self.layers:
            layer = self.layers[key]
            resultImg = alphaMergeImage3D(layer, resultImg)
        if self.resultFace:
            coefExtinctionFace = 1 - (self.countEmptyLayersHands / self.filterPowerHands)
            colorWithExtinction = list(np.dot(self.colorPointsFace, coefExtinctionFace))
            resultImg = drawFace.drawPointsOnImg(resultImg, self.resultFace['lmList'], pointFaceRadius, colorWithExtinction,
                                                  pointsFaceThickness)
        if self.resultHands:
            coefExtinctionHand = 1 - (self.countEmptyLayersHands / self.filterPowerHands)
            for typeHand in self.resultHands:
                for i, color in enumerate(self.colorLinesHand[typeHand]):
                    self.colorLinesHand[typeHand][i] = list(np.dot(color, coefExtinctionHand))
                if typeHand in self.resultHands and typeHand in self.colorLinesHand:
                    resultImg = drawHand.drawLinesOnImgFromPoints(resultImg, self.resultHands[typeHand]['lmList'], self.colorLinesHand[typeHand], linesHandThickness)
        return resultImg

class connectGetTrackingObjects():
    def __init__(self, host='localhost', port=8080):
        if host == 'localhost': self.host = f'http://127.0.0.1:{port}/'
        else: self.host = host

    def postImage(self, img, endpoint):
        imgString = encodeImage(img)
        try:
            response = requests.post(url=f'{self.host}{endpoint}', data=imgString)
            if response.status_code != 200:
                print(f'Bad code: {response.status_code}')
                return None
        except:
            print('Bad connection')
            return None
        return response

    def getResponseByImage(self, img, endPoint):
        response = self.postImage(img, endpoint=endPoint)
        if response is None: return None
        bytesStringData = response.content
        stringData = bytesStringData.decode('utf-8')
        data = json.loads(stringData)
        return data

    def getPositionFaces(self, img):
        return self.getResponseByImage(img, 'img/get-tracking/face/lines')

    def getPositionHands(self, img):
        return self.getResponseByImage(img, 'img/get-tracking/hand/lines')

    def getGestureByImage(self, img):
        return self.getResponseByImage(img, 'img/get-gesture')

def showWindowError():
    height, width = 600, 800
    textFont = cv2.FONT_HERSHEY_SIMPLEX
    zeroImg = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.putText(zeroImg, '[ERROR]', (210, 300), textFont, 3, (255, 255, 255), 3)
    cv2.putText(zeroImg, '<check the console for more info>', (260, 360), textFont, 0.5, (255, 255, 255), 1)
    cv2.imshow('Camera', zeroImg)

def showCamera():
    global mainImg, run, indexGesture, allGestureNames
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FPS, 30)
    try:
        while run:
            success, mainFlipImg = cap.read()
            mainImg = cv2.flip(mainFlipImg, 2)
            if success:
                resultImg = outputWorker.getResultImg(mainImg)
                cv2.imshow('Camera', resultImg)
            match cv2.waitKey(1):
                case 27: run = False
                # case 83:
                #     indexGesture = (indexGesture + 1) % len(allGestureNames)
                #     sleep(0.1)
                # case 81:
                #     indexGesture = (indexGesture - 1) if (indexGesture - 1) >= 0 else len(allGestureNames)-1
                #     sleep(0.1)
    except Exception:
        print(format_exc())
        cv2.destroyAllWindows()
        showWindowError()
        while run:
            if cv2.waitKey(1) == 27: run = False

def computingFunction():
    global mainImg, run, indexGesture, allGestureNames
    mainImg = None
    oldGestureData = {}
    # allGestureNames = db.getStaticGesturesNames()
    # indexGesture = 0
    while run:
        if mainImg is None: continue
        # gestureName = allGestureNames[indexGesture]
        # fullGesture = db.getStaticGesture(gestureName)
        compressedImg = compressImage(mainImg, 70)

        hands = con.getPositionHands(compressedImg)
        onlyMainHands = handWorker.getOnlyMainHands(hands)
        resultHands = handWorker.getResultHands(onlyMainHands, filterPower=2, confidence=0.78)
        resultFace = {}
        gestureName = None

        if resultHands:
            faces = con.getPositionFaces(compressedImg)
            onlyOneFace = faceWorker.getOnlyOneFace(faces)
            resultFace = faceWorker.getResultFace(onlyOneFace, filterPower=2)

            gestureType, gestureName, handPercent, lineHandsPercent = handWorker.getMaxPossibleGesture(resultHands, resultFace, db.get(), oldGestureData)
            # lineHandsPercent = handWorker.getLineHandsPercent(resultHands, fullGesture, resultFace)
            colorLinesHand = drawHand.getColorLinesHand(resultHands, lineHandsPercent)
            outputWorker.setColorLinesHand(colorLinesHand)
            oldGestureData = dict(type=gestureType, name=gestureName, percent=handPercent)

        zeroImg = getZero3DImage(mainImg.shape[:2])
        nameGestuneOnScreen = drawTextOnImage(zeroImg, gestureName, (70, 650), 2, (255, 255, 255), 3)
        outputWorker.setLayer('nameGesture', nameGestuneOnScreen)
        outputWorker.setLinesFromHands(resultHands)
        outputWorker.setLinesFromFace(resultFace)


def main():
    thShowCamera = Thread(target=showCamera)
    thShowCamera.start()
    thComputingFunction = Thread(target=computingFunction)
    thComputingFunction.start()

if __name__ == '__main__':
    run = True
    outputWorker = outputImageWorker()
    con = connectGetTrackingObjects(host='localhost')
    main()