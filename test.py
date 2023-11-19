from ModuleHandWorking import globalHandWorker, drawHandWorker, handDetector
from ModuleFaceWorking import globalFaceWorker, drawFaceWorker, faceDetector
import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FPS, 30)
    detectorH = handDetector(detectionCon=0.8, maxHands=4)
    detectorF = faceDetector(detectionCon=0.8, maxFaces=1)
    while cv2.waitKey(1) != 27:
        success, img = cap.read()
        height, width = img.shape[:2]
        zeroImg = np.zeros((height, width, 3), dtype=np.uint8)
        hands = detectorH.findHands(img)
        faces = detectorF.findFaces(img)
        if success:
            if hands and faces:
                for hand in hands:
                    zeroImg = drawHand.drawLinesOnImgFromPoints(zeroImg, hand["lmList"], [(0, 210, 0)] * 21, 4)
                for face in faces:
                    zeroImg = drawFace.drawPointsOnImg(zeroImg, face["lmList"], 1, (0, 210, 0), 2)
                #cv2.line(zeroImg, list(map(int, list(hands[0]['lmList'][8].values())[:2])), list(map(int, list(faces[0]['lmList'][30].values())[:2])), (0, 0, 240), 2)
                cv2.line(zeroImg, (400, 400), (1000, 400), (255, 255, 255), 1)
                cv2.line(zeroImg, (700, 100), (700, 700), (255, 255, 255), 1)
                cv2.imshow("Image-lines", zeroImg)
            cv2.imshow("Image", img)


if __name__ == "__main__":
    handWorker = globalHandWorker()
    drawHand = drawHandWorker()
    faceWorker = globalFaceWorker()
    drawFace = drawFaceWorker()
    main()

