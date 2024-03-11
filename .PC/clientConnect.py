from PC.modules.handWorking import globalHandWorker, drawHandWorker
from PC.modules.faceWorking import globalFaceWorker, drawFaceWorker
from db.database import dbWorker
from PC.modules.imageWorking import *
from traceback import format_exc
from threading import Thread
from time import sleep
import numpy as np
import requests
import json
import cv2

PATH2DB = 'gestures/dactyl.json'
db = dbWorker(PATH2DB)
handWorker = globalHandWorker()
faceWorker = globalFaceWorker()
drawHand = drawHandWorker()
drawFace = drawFaceWorker()

class outputImageWorker():
    def __init__(self):
        self.layers = {}
        self.texts = {}
        self.resultHands = {}
        self.resultFace = {}

    def setLayer(self, name, img, color):
        self.layers[name] = {'image': img, 'color': color}

    def setText(self, name, data):
        self.texts[name] = data

    def setColorLinesHand(self, colorLinesHand):
        self.colorLinesHand = colorLinesHand

    def setColorPointsFace(self, colorPointsFace):
        self.colorPointsFace = colorPointsFace

    def setLinesFromHands(self, resultHands):
        if resultHands is None: return
        self.resultHands = resultHands

    def setLinesFromFace(self, resultFace):
        if resultFace is None: return
        self.resultFace = resultFace

    def getResultImg(self, background, linesHandThickness=3, pointsFaceThickness=2, pointFaceRadius=1):
        resultImg = addAlphaInImage(background)
        if self.resultFace and self.colorPointsFace:
            zeroImg = getZero4DImage(resultImg.shape)
            faceImg = drawFace.drawPointsOnImg(zeroImg, self.resultFace['lmList'], pointFaceRadius, self.colorPointsFace, pointsFaceThickness)
            resultImg = alphaMergeImage4D(resultImg, faceImg)
        if self.resultHands:
            for typeHand in self.resultHands:
                if not (typeHand in self.resultHands and typeHand in self.colorLinesHand): continue
                resultImg = drawHand.drawLinesOnImgFromPoints(resultImg, self.resultHands[typeHand]['lmList'], self.colorLinesHand[typeHand], linesHandThickness)
        for key, layer in self.layers.items():
            resultImg = alphaMergeImage3D(resultImg, layer['image'], layer['color'])
        for key, text in self.texts.items():
            resultImg = setTextOnImage(resultImg, text)
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
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.set(28, 0)
    try:
        while run:
            success, mainFlipImg = cap.read()
            mainImg = cv2.flip(mainFlipImg, 2)
            if success:
                resultImg = outputWorker.getResultImg(mainImg)
                coef = 1
                resultImg = cv2.resize(resultImg, (int(resultImg.shape[1] * coef), int(resultImg.shape[0] * coef)))
                cv2.imshow('Camera', resultImg)
            match cv2.waitKey(1):
                case 27: run = False
                case 83:
                    indexGesture = (indexGesture + 1) % len(allGestureNames)
                    sleep(0.1)
                case 81:
                    indexGesture = (indexGesture - 1) if (indexGesture - 1) >= 0 else len(allGestureNames)-1
                    sleep(0.1)
    except Exception:
        print(format_exc())
        cv2.destroyAllWindows()
        showWindowError()
        while run:
            if cv2.waitKey(1) == 27: run = False

def computingFunction():
    global mainImg, run, indexGesture, allGestureNames
    mainImg = None
    allGestureNames = db.getStaticGesturesNames()
    indexGesture = 0
    while run:
        if mainImg is None: continue
        gestureName = allGestureNames[indexGesture]
        fullGesture = db.getStaticGesture(gestureName)
        compressedImg = compressImage(mainImg, 70)

        realHands = con.getPositionHands(compressedImg)
        resultHands = handWorker.getResultHands(realHands)
        resultFace = {}
        if resultHands:
            realFaces = con.getPositionFaces(compressedImg)
            resultFace = faceWorker.getResultFace(realFaces)
            needFacePointsByHand = faceWorker.getNeedPointsByHand(fullGesture)

            lineHandsPercent = handWorker.getLineHandsPercent(resultHands, fullGesture, resultFace)
            colorLinesHand = drawHand.getColorLinesHand(resultHands, lineHandsPercent)
            colorPointsFace = drawFace.getColorPointsFace(needFacePointsByHand, resultFace, [170, 80, 70, 255], 70)
            outputWorker.setColorLinesHand(colorLinesHand)
            outputWorker.setColorPointsFace(colorPointsFace)

        textData = dict(string=gestureName, pos=(70, 650), scale=2, color=(0, 40, 240), thickness=3)
        outputWorker.setText('nameGesture', textData)
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