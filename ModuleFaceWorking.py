import cv2
import mediapipe as mp
import numpy as np
import multiprocessing
from copy import copy
from math import sqrt
from ModuleImageWorking import *

class faceDetector():
    def __init__(self, mode=False, maxFaces=1, detectionCon=0.5, minTrackCon=0.5):
        self.mode = mode
        self.maxFaces = maxFaces
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=self.mode, max_num_faces=self.maxFaces,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)


    def getResults(self, imgRGB):
        self.results = self.faceMesh.process(imgRGB)

    def findFaces(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        processFinding = multiprocessing.Process(self.getResults(imgRGB))
        while processFinding.is_alive(): pass
        self.height, self.width = img.shape[:2]
        allFaces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                lmList = []
                for lm in faceLms.landmark:
                    px, py, pz = lm.x * self.width, lm.y * self.height, lm.z * self.width
                    lmList.append(dict(x=px, y=py, z=pz))
                allFaces.append({
                    'lmList': lmList
                })
        return allFaces

class drawFaceWorker():
    def drawPointsOnImg(self, img, lmList, radius, colorPoints, thickness):
        resultImg = copy(img)
        for point in colorPoints:
            cv2.circle(resultImg, (int(lmList[point]['x']), int(lmList[point]['y'])),
                       radius, colorPoints[point], thickness)
        return resultImg

    def getDistanceBetweenPoints(self, point1, point2):
        vector = {axis: (point1[axis] - point2[axis]) for axis in ['x', 'y', 'z']}
        lengthVector = sqrt(vector['x'] ** 2 + vector['y'] ** 2 + vector['z'] ** 2)
        return lengthVector

    def getColorPointsFace(self, needPointsByHand, face, maxColor, maxCount):
        if not needPointsByHand or not face: return {}
        colorPointsFace = {}
        for point in needPointsByHand:
            pos1 = face['lmList'][point]
            lens = {j: self.getDistanceBetweenPoints(pos1, pos2) for j, pos2 in enumerate(face['lmList'])}
            lens = {k: v for k, v in sorted(lens.items(), key=lambda item: item[1])}
            for count, key in enumerate(lens):
                if count == maxCount: break
                colorPointsFace[key] = np.dot(maxColor, ((maxCount - count) / maxCount))
        return colorPointsFace

class globalFaceWorker():
    def getResultFace(self, realFaces):
        if not realFaces: return []
        resultFace = realFaces[-1]
        return resultFace

    def getNeedPointsByHand(self, fullGesture):
        if not fullGesture['useFace']: return None
        needPointsByHand = [parm[1] for parm in fullGesture['linkedPointsWithFace']]
        return needPointsByHand

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FPS, 30)
    detector = faceDetector(detectionCon=0.8, maxFaces=1)
    while cv2.waitKey(1) != 27:
        success, img = cap.read()
        height, width = img.shape[:2]
        zeroImg = np.zeros((height, width, 3), dtype=np.uint8)
        faces = detector.findFaces(img)
        if success:
            if faces:
                for face in faces:
                    zeroImg = drawFace.drawPointsOnImg(zeroImg, face["lmList"], 1, (0, 210, 0), 2)
                cv2.imshow("Image-lines", zeroImg)
            cv2.imshow("Image", img)


if __name__ == "__main__":
    faceWorker = globalFaceWorker()
    drawFace = drawFaceWorker()
    main()
