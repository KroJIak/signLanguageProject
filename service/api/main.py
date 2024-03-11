from fastapi import FastAPI
from pydantic import BaseModel

serviceApp = FastAPI()

class ImageRequest(BaseModel):
    base64String: bytes
    width: int
    height: int

class Response(BaseModel):
    points: dict

@serviceApp.post('/detection/dictionary/{dictId}/gesture/{gestName}')
async def detectionGestureOnImage(image: ImageRequest, dictId: int, gestName: str):
    print(dictId, gestName)
    return PointsResponse(points={})


@serviceApp.options('/detection/dictionary/{dictId}/gesture/{gestName}')
async def optionsImage(): return