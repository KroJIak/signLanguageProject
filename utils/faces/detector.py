
import time
import multiprocessing

from utils.objects import Point
from utils.faces.objects import Face

import mediapipe as mp
import cv2

class FaceDetector:
    def __init__(self, maxFaces=1, detectionCon=0.5, minTrackCon=0.5, staticImage=False, timer=0.3):
        self.maxFaces = maxFaces
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.staticImage = staticImage
        self.timer = timer

        self.results = None
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=False, max_num_faces=self.maxFaces,
                                                 min_detection_confidence=self.detectionCon,
                                                 min_tracking_confidence=self.minTrackCon)

    def updateResults(self, imgRGB):
        self.results = self.faceMesh.process(imgRGB)

    def findFaces(self, img):
        self.height, self.width = img.shape[:2]
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lastTime = time.time()
        while lastTime + self.timer > time.time():
            processFinding = multiprocessing.Process(self.updateResults(imgRGB))
            while processFinding.is_alive(): pass
            if not self.staticImage: break
        allFaces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                lmList = []
                for id, lm in enumerate(faceLms.landmark):
                    px, py, pz = lm.x * self.width, lm.y * self.height, lm.z * self.width
                    lmList.append(Point(px, py, pz, id))
                allFaces.append(Face(lmList))
        return allFaces