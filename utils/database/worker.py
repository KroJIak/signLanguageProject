import json
import os

from utils.database.const import ConstPlenty
from utils.funcs import joinPath

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