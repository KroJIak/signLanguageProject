
from utils.database.worker import dbDictGlobalWorker, dbGlobalWorker
from db.modules.const import ConstPlenty

const = ConstPlenty()

class dbDictWorker(dbDictGlobalWorker):
    def getDictionaries(self):
        dbData = self.get()
        return dbData

    def getDictionaryName(self, dictId):
        dbData = self.get()
        dictionaryName = dbData[str(dictId)]
        return dictionaryName

class dbGesturesWorker(dbGlobalWorker):
    def getGestures(self):
        dbData = self.get()
        return dbData

    def getGestureNames(self):
        dbData = self.get()
        gestureName = tuple(sorted(dbData.keys()))
        return gestureName