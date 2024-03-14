from fastapi import FastAPI
from pydantic import BaseModel
from service.utils.const import Point, Line
from service.modules.imageWorking import base64ToImage
from service.modules.globalWorking import getResultShapes
from time import time


serviceApp = FastAPI()

class ImageRequest(BaseModel):
    base64String: bytes

class ShapesResponse(BaseModel):
    points: list[Point]
    lines: list[Line]
    startTime: float

@serviceApp.post('/detection/dictionary/{dictId}/gesture/{gestName}')
async def detectionGestureOnImage(image: ImageRequest, dictId: int, gestName: str):
    startTime = time()
    img = base64ToImage(image.base64String[23:])
    points, lines = getResultShapes(img, dictId, gestName)
    return ShapesResponse(points=points, lines=lines, startTime=startTime)

@serviceApp.options('/detection/dictionary/{dictId}/gesture/{gestName}')
async def optionsImage(): return