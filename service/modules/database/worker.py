
from utils.database.worker import dbDictGlobalWorker, dbGlobalWorker
from utils.hands.objects import Gesture, Hand, BoneVector
from utils.objects import LinkedPoint

class dbDictWorker(dbDictGlobalWorker):
    def getDictionaries(self):
        dbData = self.get()
        return dbData

    def getDictionaryName(self, dictId):
        dbData = self.get()
        dictionaryName = dbData[str(dictId)]
        return dictionaryName

class dbGestureWorker(dbGlobalWorker):
    def getGestures(self):
        dbData = self.get()
        return dbData

    def getGesture(self, name):
        dbData = self.get()
        dictGesture = dbData[name]
        hands = []
        for typeHand, dictHand in dictGesture.items():
            bones = []
            for dictBone in dictHand['bones']:
                dictVector = dictBone['vector']
                boneVector = BoneVector(dictVector['x'], dictVector['y'], dictVector['z'], dictBone['id'], dictBone['parentId'])
                bones.append(boneVector)
            linkedPoints = []
            for dictLinkedPoint in dictHand['linkedPoints']:
                linkedPoint = LinkedPoint(dictLinkedPoint['handPointId'], dictLinkedPoint['facePointId'], dictLinkedPoint['dist'])
                linkedPoints.append(linkedPoint)
            resultHand = Hand(typeHand, bones=bones, useFace=dictHand['useFace'], linkedPoints=linkedPoints)
            hands.append(resultHand)
        resultGesture = Gesture(name, hands)
        return resultGesture