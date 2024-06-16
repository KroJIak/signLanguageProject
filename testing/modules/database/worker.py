
from utils.database.worker import dbDictGlobalWorker, dbGestureGlobalWorker

class dbDictWorker(dbDictGlobalWorker):
    def getDictionaries(self):
        dbData = self.get()
        return dbData

    def getDictionaryName(self, dictId):
        dbData = self.get()
        dictionaryName = dbData[str(dictId)]
        return dictionaryName

class dbGestureWorker(dbGestureGlobalWorker):
    def __init__(self, databasePath):
        super().__init__(databasePath)