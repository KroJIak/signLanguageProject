from PC.modules.handWorking import handDetector, globalHandWorker, drawHandWorker
from db.database import dbWorker
import os
import cv2

PATH2DB = 'gestures/dactyl.json'
db = dbWorker(PATH2DB)

def main():
    detectorStaticImages = handDetector(mode=True, detectionCon=0.3, minTrackCon=0.6, maxHands=2)
    handWorker = globalHandWorker()
    drawHand = drawHandWorker()

    folderPath = 'gestures/assets/custom/'
    GestureNameFiles = os.listdir(folderPath)
    undetectedGestures = set()
    for file in GestureNameFiles:
        imgGesture = cv2.imread(f'{folderPath}/{file}')
        gestureName = file[:file.rfind('.')]
        hands = detectorStaticImages.findHands(imgGesture, flipType=False)
        onlyMainHands = handWorker.getOnlyMainHands(hands)
        if not onlyMainHands:
            undetectedGestures.add(gestureName)
            continue
        db.addStaticGesture(gestureName, onlyMainHands)
        if len(onlyMainHands) == 1: db.addNameStaticGestureToOneHandsList(gestureName)
        elif len(onlyMainHands) == 2: db.addNameStaticGestureToTwoHandsList(gestureName)
        linesHands = handWorker.onlyMainHands2LmList(onlyMainHands)
        for lmList in linesHands:
            imgGesture = drawHand.drawLinesOnImgFromPoints(imgGesture, lmList, [(0, 210, 0)]*21, 3)
        cv2.imshow('Gesture', imgGesture)
        while cv2.waitKey(1) != 27: pass
    print(f'Undetected gestures: {undetectedGestures}')

if __name__ == '__main__':
    main()