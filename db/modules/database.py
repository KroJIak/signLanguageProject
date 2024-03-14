import json
import os
from db.modules.const import Error

error = Error()

class dbWorker():
    def __init__(self, databasePath, fileName):
        self.databasePath = databasePath
        self.fileName = fileName
        if not self.isExists():
            raise ValueError(error.dbDoesNotExist())

    def isExists(self):
        files = os.listdir(self.databasePath)
        return self.fileName in files

    def get(self):
        with open(self.databasePath + self.fileName) as file:
            dbData = json.load(file)
        return dbData

    def save(self, dbData):
        with open(self.databasePath + self.fileName, 'w', encoding='utf-8') as file:
            json.dump(dbData, file, indent=4, ensure_ascii=False)

class dbDictionariesWorker(dbWorker):
    def getDictionaries(self):
        dbData = self.get()
        dictionaries = dbData['indexation']
        return dictionaries

    def getDictionaryName(self, dictId):
        dbData = self.get()
        dictionaryName = dbData['indexation'][str(dictId)]
        return dictionaryName

class dbGesturesWorker(dbWorker):
    def getAllGestures(self):
        dbData = self.get()
        return dbData

    def getGestureNames(self):
        dbData = self.get()
        gestureName = tuple(dbData.keys())
        return gestureName

    def getGesutre(self, name):
        dbData = self.get()
        if name not in dbData: raise ValueError(error.gestureDoesNotExist())
        gesture = dbData[name]
        return gesture

def getDictionaryFileName(path, dictId):
    dbDictionaries = dbDictionariesWorker(path, 'database.json')
    dictionaryName = dbDictionaries.getDictionaryName(dictId)
    dictionaryFileName = f'{dictionaryName}.json'
    return dictionaryFileName