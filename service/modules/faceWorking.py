import multiprocessing
import mediapipe as mp
from service.utils.const import ConstPlenty, Position, Point, Line
from pydantic import BaseModel
from service.utils.funcs import *
import cv2

class Face(BaseModel):
    lmList: list

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
                allFaces.append(Face(lmList=lmList))
        return allFaces

def getLinkedFacePoints(masterGesture):
    if not masterGesture['useFace']: return ()
    facePoints = tuple(map(lambda x: x[1], masterGesture['linkedPointsWithFace'] ))
    return facePoints

'''def getPointsFromFace(faces, color=(60, 60, 240, 0.4), radius=1.5):
    if not faces: return []
    face = faces[-1]
    points = []
    for realPos in face.lmList:
        screenPos = Position(x=int(realPos['x']), y=int(realPos['y']))
        points.append(Point(pos=screenPos, color=color, radius=radius))
    return points'''

def getPointsFromFace(faces, masterGesture, maxColor=(60, 60, 240), maxCount=70, radius=1.5):
    if not faces: return []
    face = faces[-1]
    resutlPoints = []
    linkedFacePoints = getLinkedFacePoints(masterGesture)
    for pnt in linkedFacePoints:
        pos1 = face.lmList[pnt]
        distances = {j: getDistanceBetweenPoints(pos1, pos2, thirdDim=True) for j, pos2 in enumerate(face.lmList)}
        distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
        for count, key in enumerate(distances):
            if count == maxCount: break
            resultColor = list(maxColor) + [(maxCount - count) / maxCount]
            resultPos = Position(x=int(face.lmList[key]['x']), y=int(face.lmList[key]['y']))
            resutlPoints.append(Point(pos=resultPos, color=resultColor, radius=radius))
    return resutlPoints

