import cv2
import mediapipe as mp
import numpy as np
import multiprocessing
from copy import copy

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
    def drawPointsOnImg(self, img, lmList, radius, colorLines, thickness):
        resultImg = copy(img)
        for point in range(len(lmList)):
            cv2.circle(resultImg, (int(lmList[point]['x']), int(lmList[point]['y'])), radius, colorLines, thickness)
        return resultImg

class globalFaceWorker():
    def __init__(self):
        self.facesOldArr = []
        self.filterPower = 0

    def onlyOneFace2LmList(self, face):
        lmList = face['lmList']
        return lmList

    def getOnlyOneFace(self, faces):
        if faces: return faces[-1]
        else: return {}

    def getFacesOldArray(self):
        return self.facesOldArr

    def getFilterPower(self):
        return self.filterPower

    def getResultFace(self, face, filterPower):
        self.filterPower = filterPower
        self.facesOldArr.append(face)
        resultFace = self.filteringlmListByAverageValue(face, self.filterPower,
                                                        self.facesOldArr)
        self.facesOldArr = self.facesOldArr[::-1]
        self.facesOldArr = self.facesOldArr[:self.filterPower]
        self.facesOldArr = self.facesOldArr[::-1]
        return resultFace

    def filteringlmListByAverageValue(self, realFace, filterPower=0, facesOldArr=[]):
        if len(facesOldArr) <= filterPower: return realFace

        resultFace = {}
        countFullFace = 0
        for face in facesOldArr:
            if face:
                countFullFace += 1
                if 'lmList' not in resultFace:
                    resultFace = face
                else:
                    lmListFace = face['lmList']
                    for posId in range(len(lmListFace)):
                        curX = resultFace['lmList'][posId]['x']
                        curY = resultFace['lmList'][posId]['y']
                        curZ = resultFace['lmList'][posId]['z']
                        resultFace['lmList'][posId]['x'] = curX + lmListFace[posId]['x']
                        resultFace['lmList'][posId]['y'] = curY + lmListFace[posId]['y']
                        resultFace['lmList'][posId]['z'] = curZ + lmListFace[posId]['z']

        if resultFace:
            for posId in range(len(resultFace['lmList'])):
                curX = resultFace['lmList'][posId]['x']
                curY = resultFace['lmList'][posId]['y']
                curZ = resultFace['lmList'][posId]['z']
                resultFace['lmList'][posId]['x'] = curX // countFullFace
                resultFace['lmList'][posId]['y'] = curY // countFullFace
                resultFace['lmList'][posId]['z'] = curZ // countFullFace

        return resultFace

def main():
    cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
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
