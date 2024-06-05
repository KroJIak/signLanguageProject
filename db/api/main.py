
from db.modules.database.worker import dbDictWorker, dbGesturesWorker
from db.modules.const import ConstPlenty

from fastapi import FastAPI
from pydantic import BaseModel

dbApp = FastAPI()
const = ConstPlenty()
dbDictionaries = dbDictWorker()

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
    dictionaryName = dbDictionaries.getDictionaryName(dictId)
    dictionaryPath = dbDictionaries.getDictionaryPath(dictionaryName)
    dbGestures = dbGesturesWorker(dictionaryPath)
    gestureNames = dbGestures.getGestureNames()
    return GestureNamesResponse(gestureNames=gestureNames)
