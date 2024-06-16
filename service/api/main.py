import time

from service.modules.image import base64ToImage
from service.modules.front.main import getResultShapes
from service.modules.objects import WebLine, WebPoint

from fastapi import FastAPI
from pydantic import BaseModel

serviceApp = FastAPI()

class ImageRequest(BaseModel):
    base64String: bytes

class ShapesResponse(BaseModel):
    points: list[WebPoint]
    lines: list[WebLine]
    startTime: float

# Упал, вставай. Встал – упай. Пай чокопай

@serviceApp.post('/detection/dictionary/{dictId}/gesture/{gestureName}')
async def detectionGestureOnImage(image: ImageRequest, dictId: int, gestureName: str):
    startTime = time.time()
    img = base64ToImage(image.base64String[23:])
    points, lines = getResultShapes(img, dictId, gestureName)
    return ShapesResponse(points=points, lines=lines, startTime=startTime)

@serviceApp.options('/detection/dictionary/{dictId}/gesture/{gestureName}')
async def optionsImage(): return