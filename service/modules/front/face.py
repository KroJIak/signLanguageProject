
from service.modules.const import WebPoint, WebPosition
from service.modules.funcs import *

def getLinkedFacePointIds(masterGesture):
    facePointIds = []
    for hand in masterGesture.hands:
        if not hand.useFace: continue
        for linkedPoint in hand.linkedPoints:
            facePointIds.append(linkedPoint.facePointId)
    return tuple(facePointIds)

def getPointsFromFace(faces, masterGesture, maxColor=(60, 60, 240), maxCount=70, radius=1.5):
    if not faces: return []
    face = faces[-1]
    resutlPoints = []
    linkedFacePointIds = getLinkedFacePointIds(masterGesture)
    for pointId in linkedFacePointIds:
        point1 = face.lmList[pointId]
        distances = {j: getDistanceBetweenPoints(point1, point2) for j, point2 in enumerate(face.lmList)}
        distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
        for count, key in enumerate(distances):
            if count == maxCount: break
            resultColor = list(maxColor) + [(maxCount - count) / maxCount]
            webPosition = WebPosition(x=int(face.lmList[key].x), y=int(face.lmList[key].y))
            resutlPoints.append(WebPoint(pos=webPosition, color=resultColor, radius=radius))
    return resutlPoints

