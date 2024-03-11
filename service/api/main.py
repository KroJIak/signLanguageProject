from fastapi import FastAPI
from pydantic import BaseModel

serviceApp = FastAPI()

class ImageRequest(BaseModel):
    base64String: bytes

class ImageResponse(BaseModel):
    base64String: bytes

class ShapesResponse(BaseModel):
    points: list
    lines: list
    circles: list

@serviceApp.post('/detection/dictionary/{dictId}/gesture/{gestName}')
async def detectionGestureOnImage(image: ImageRequest, dictId: int, gestName: str):
    points = []
    lines = []
    circles = []
    return ShapesResponse(points=points, lines=lines, circles=circles)


@serviceApp.options('/detection/dictionary/{dictId}/gesture/{gestName}')
async def optionsImage(): return