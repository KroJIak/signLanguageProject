
from utils.database.worker import dbDictGlobalWorker, dbGestureGlobalWorker

class dbDictWorker(dbDictGlobalWorker):
    def getNextDictId(self):
        dbData = self.get()
        if not len(dbData.keys()): return '0'
        maxId = max(list(map(int, dbData.keys())))
        nextId = maxId + 1
        return str(nextId)

    def addNewDictionary(self, name):
        dbData = self.get()
        if name in dbData.values(): return
        dictId = self.getNextDictId()
        dbData[dictId] = name
        self.save(dbData)

    def replaceDictionary(self, name):
        dbData = self.get()
        if name in dbData.values():
            keyByName = list(dbData.keys())[list(dbData.values()).index(name)]
            del dbData[keyByName]
        self.addNewDictionary(name)

class dbGestureWorker(dbGestureGlobalWorker):
    def __init__(self, databasePath):
        super().__init__(databasePath)

    def addNewGesture(self, gesture):
        dbData = self.get()
        if gesture.name in dbData: return
        dbData[gesture.name] = {}
        for hand in gesture.hands:
            bones = [{'id': bone.id, 'parentId': bone.parentId,
                      'vector': {'x': bone.x, 'y': bone.y, 'z': bone.z}}
                      for bone in hand.bones]
            normalVector = hand.normalVector
            linkedPoints = [{'handPointId': point.handPointId, 'facePointId': point.facePointId,
                             'dist': point.dist} for point in hand.linkedPoints]
            dbData[gesture.name][hand.typeHand] = {
                'bones': bones,
                'normalVector': {'x': normalVector.x, 'y': normalVector.y, 'z': normalVector.z},
                'useFace': hand.useFace,
                'linkedPoints': linkedPoints
            }
        self.save(dbData)

    def replaceGesture(self, gesture):
        dbData = self.get()
        if gesture.name in dbData: del dbData[gesture.name]
        self.addNewGesture(gesture)