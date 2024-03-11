from fastapi import FastAPI
from pydantic import BaseModel

dbApp = FastAPI()

class Response(BaseModel):
    dictId: int
    gestName: str

@dbApp.post('/dictionary/{dictId}/gesture/{gestName}')
async def getGesture(dictId: int, gestName: str):
    return Response(dictId=dictId, gestName=gestName)