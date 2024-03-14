from db.modules.database import dbGesturesWorker, getDictionaryFileName
from service.utils.const import ConstPlenty
from service.modules.handWorking import handDetector, getResultLineHands, getPointsFromHands
from service.modules.faceWorking import faceDetector, getPointsFromFace

const = ConstPlenty()
detHands = handDetector(detectionCon=0.6, minTrackCon=0.6, maxHands=2)
detFaces = faceDetector(detectionCon=0.6, minTrackCon=0.6, maxFaces=1)

def getMasterGesture(dictId, gestName):
    dictionaryFileName = getDictionaryFileName(const.mainPath + const.path.gestures, dictId)
    dbGestures = dbGesturesWorker(const.mainPath + const.path.dictionaries, dictionaryFileName)
    masterGesture = dbGestures.getGesutre(gestName)
    return masterGesture

def getResultShapes(img, dictId, gestName):
    masterGesture = getMasterGesture(dictId, gestName)
    realHands = detHands.findHands(img)
    realFaces = detFaces.findFaces(img)
    resultPoints = getPointsFromFace(realFaces, masterGesture) + getPointsFromHands(realHands)
    resultLines = getResultLineHands(realHands, realFaces, masterGesture)
    return resultPoints, resultLines