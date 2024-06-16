import json
import os

from utils.database.const import ConstPlenty
from utils.funcs import joinPath

from utils.objects import Vector, LinkedPoint
from utils.hands.objects import BoneVector, Hand, Gesture

const = ConstPlenty()

class dbGlobalWorker():
    def __init__(self, databasePath):
        folderPath = databasePath.split('/')
        self.fileName = folderPath.pop(-1)
        self.folderPath = '/'.join(folderPath)
        if not self.isExists(): self.save({})

    def isExists(self):
        files = os.listdir(self.folderPath)
        return self.fileName in files

    def get(self):
        with open(joinPath(self.folderPath, self.fileName)) as file:
            dbData = json.load(file)
        return dbData

    def save(self, dbData):
        with open(joinPath(self.folderPath, self.fileName), 'w', encoding='utf-8') as file:
            json.dump(dbData, file, indent=4, ensure_ascii=False)

class dbDictGlobalWorker(dbGlobalWorker):
    def __init__(self):
        super().__init__(const.path.file.indexations)

    def getDictionaryPath(self, name):
        dictionaryPath = joinPath(const.path.dictionaries, f'{name}.json')
        return dictionaryPath

class dbGestureGlobalWorker(dbGlobalWorker):
    def __init__(self, databasePath):
        super().__init__(databasePath)

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
                boneVector = BoneVector(*list(dictVector.values()), dictBone['id'], dictBone['parentId'])
                bones.append(boneVector)
            dictNormalVector = dictHand['normalVector']
            normalVector = Vector(*list(dictNormalVector.values()))
            linkedPoints = []
            for dictLinkedPoint in dictHand['linkedPoints']:
                linkedPoint = LinkedPoint(dictLinkedPoint['handPointId'], dictLinkedPoint['facePointId'],
                                          dictLinkedPoint['dist'])
                linkedPoints.append(linkedPoint)
            resultHand = Hand(typeHand, bones=bones, normalVector=normalVector, useFace=dictHand['useFace'],
                              linkedPoints=linkedPoints)
            hands.append(resultHand)
        resultGesture = Gesture(name, hands)
        return resultGesture