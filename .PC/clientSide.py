from PC.modules.handWorking import globalHandWorker, drawHandWorker, handDetector
from PC.modules.faceWorking import globalFaceWorker, drawFaceWorker, faceDetector
from db.database import dbWorker
from PC.modules.imageWorking import *

PATH2DB = 'gestures/dactyl.json'
db = dbWorker(PATH2DB)

detHands = handDetector(detectionCon=0.6, minTrackCon=0.6, maxHands=2)
detFaces = faceDetector(detectionCon=0.6, minTrackCon=0.6, maxFaces=1)
handWorker = globalHandWorker()
faceWorker = globalFaceWorker()
drawHand = drawHandWorker()
drawFace = drawFaceWorker()

def getdbSize():
    allGestureNames = db.getStaticGesturesNames()
    return len(allGestureNames)

def getRenderedImage(background, resultHands, colorLinesHand, resultFace, colorPointsFace, linesHandThickness, pointsFaceThickness, pointFaceRadius):
    resultImg = background.copy()
    if resultFace and colorPointsFace:
        resultImg = drawFace.drawPointsOnImg(resultImg, resultFace['lmList'], pointFaceRadius, colorPointsFace, pointsFaceThickness)
    if resultHands:
        for typeHand in resultHands:
            resultImg = drawHand.drawLinesOnImgFromPoints(resultImg, resultHands[typeHand]['lmList'], colorLinesHand[typeHand], linesHandThickness)
    return resultImg

def getResultImage(mainImg, indexGesture, linesHandThickness=3, pointsFaceThickness=2, pointFaceRadius=1):
    allGestureNames = db.getStaticGesturesNames()
    gestureName = allGestureNames[indexGesture]
    fullGesture = db.getStaticGesture(gestureName)

    zeroImg = getZero4DImage(mainImg.shape)
    realHands = detHands.findHands(mainImg, flipType=False)
    resultHands = handWorker.getResultHands(realHands)
    resultFace, colorPointsFace = {}, {}
    if resultHands:
        realFaces = detFaces.findFaces(mainImg)
        resultFace = faceWorker.getResultFace(realFaces)
        needFacePointsByHand = faceWorker.getNeedPointsByHand(fullGesture)
    lineHandsPercent = handWorker.getLineHandsPercent(resultHands, fullGesture, resultFace)
    colorLinesHand = drawHand.getColorLinesHand(resultHands, lineHandsPercent)
    if resultFace: colorPointsFace = drawFace.getColorPointsFace(needFacePointsByHand, resultFace, [170, 80, 70, 255], 60)

    resultImg = getRenderedImage(zeroImg, resultHands, colorLinesHand, resultFace, colorPointsFace, linesHandThickness, pointsFaceThickness, pointFaceRadius)
    return resultImg


if __name__ == '__main__':
    getResultImage(None, 0)