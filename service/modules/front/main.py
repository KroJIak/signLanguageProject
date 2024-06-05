
from service.modules.const import ConstPlenty
from utils.hands.detector import HandDetector
from utils.faces.detector import FaceDetector
from service.modules.front.hand import getPointsFromHands, getResultLineHands
from service.modules.front.face import getPointsFromFace
from service.modules.database.worker import dbDictWorker, dbGestureWorker

const = ConstPlenty()
detHands = HandDetector(detectionCon=0.6, minTrackCon=0.6, maxHands=2)
detFaces = FaceDetector(detectionCon=0.6, minTrackCon=0.6, maxFaces=1)
dbDictionaries = dbDictWorker()

def getMasterGesture(dictId, gestureName):
    dictionaryName = dbDictionaries.getDictionaryName(dictId)
    dictionaryPath = dbDictionaries.getDictionaryPath(dictionaryName)
    dbGestures = dbGestureWorker(dictionaryPath)
    masterGesture = dbGestures.getGesture(gestureName)
    return masterGesture

def getResultShapes(img, dictId, gestureName):
    realHands = detHands.findHands(img)
    realFaces = detFaces.findFaces(img)
    masterGesture = getMasterGesture(dictId, gestureName)
    resultPoints = getPointsFromHands(realHands) + getPointsFromFace(realFaces, masterGesture)
    resultLines = getResultLineHands(realHands, realFaces, masterGesture)
    return resultPoints, resultLines