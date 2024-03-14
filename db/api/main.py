from fastapi import FastAPI
from pydantic import BaseModel
from db.modules.database import dbDictionariesWorker, dbGesturesWorker, getDictionaryFileName
from service.utils.const import ConstPlenty

dbApp = FastAPI()
const = ConstPlenty()
dbDictionaries = dbDictionariesWorker(const.mainPath + const.path.gestures, 'database.json')

class DictionariesResponse(BaseModel):
    dictionaries: dict

class GestureNamesResponse(BaseModel):
    gestureNames: list

@dbApp.get('/dictionaries/get-dictionaries')
async def getDictionaries():
    dictionaries = dbDictionaries.getDictionaries()
    return DictionariesResponse(dictionaries=dictionaries)

@dbApp.get('/gestures/get-gesture-names/dictionary/{dictId}')
async def getGestureNames(dictId: int):
    dictionaryFileName = getDictionaryFileName(const.mainPath + const.path.gestures, dictId)
    dbGestures = dbGesturesWorker(const.mainPath + const.path.dictionaries, dictionaryFileName)
    gestureNames = dbGestures.getGestureNames()
    return GestureNamesResponse(gestureNames=gestureNames)
