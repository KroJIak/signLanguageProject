from ModuleFaceWorking import faceDetector, globalFaceWorker, drawFaceWorker
import cv2
import numpy as np
from math import sqrt
from copy import copy


def getDistanceBetweenPoints(point1, point2):
    vector = {axis: (point1[axis] - point2[axis]) for axis in ['x', 'y', 'z']}
    lengthVector = sqrt(vector['x'] ** 2 + vector['y'] ** 2 + vector['z'] ** 2)
    return lengthVector

def drawTextOnImg(img, lmList):
    resultImg = copy(img)
    for point in range(len(lmList)):
        cv2.putText(resultImg, str(point), (int(lmList[point]['x']), int(lmList[point]['y'])), cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 0, 0), 1)
    return resultImg

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FPS, 30)
    detector = faceDetector(detectionCon=0.8, maxFaces=1)
    maxCount = 1
    while cv2.waitKey(1) != 27:
        success, img = cap.read()
        height, width = img.shape[:2]
        zeroImg = np.zeros((height, width, 3), dtype=np.uint8)
        faces = detector.findFaces(img)
        if success:
            if faces:
                for face in faces:
                    lmList = face['lmList']
                    """adjList = {}
                    for i, pos1 in enumerate(lmList):
                        lens = {j:getDistanceBetweenPoints(pos1, pos2) for j, pos2 in enumerate(lmList)}
                        lens = {k: v for k, v in sorted(lens.items(), key=lambda item: item[1])}
                        count = 0
                        for key, dist in lens.items():
                            if i == key: continue
                            if count == 6: break
                            if i not in adjList: adjList[i] = [key]
                            else: adjList[i].append(key)
                            count += 1"""

                    #zeroImg = drawFace.drawPointsOnImg(zeroImg, face["lmList"], 1, (0, 210, 0), 2)
                    zeroImg = drawTextOnImg(zeroImg, face['lmList'])
                    '''i, pos1 = 160, face['lmList'][160]
                    lens = {j: getDistanceBetweenPoints(pos1, pos2) for j, pos2 in enumerate(lmList)}
                    lens = {k: v for k, v in sorted(lens.items(), key=lambda item: item[1])}
                    count = 0
                    for key, dist in lens.items():
                        if count == maxCount: break
                        cv2.circle(zeroImg, (int(face['lmList'][key]['x']), int(face['lmList'][key]['y'])), 2, (0, 0, 255*((maxCount-count)/maxCount)), 3)
                        count += 1'''
                    # cv2.circle(zeroImg, (int(face['lmList'][0]['x']), int(face['lmList'][0]['y'])), 2, (0, 0, 255), 3)
                cv2.imshow("Image-lines", zeroImg)
                maxCount += 3
                if maxCount > 468: maxCount = 1
            cv2.imshow("Image", img)


if __name__ == "__main__":
    faceWorker = globalFaceWorker()
    drawFace = drawFaceWorker()
    main()
