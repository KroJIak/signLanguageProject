from PC.modules.handWorking import handDetector, globalHandWorker
from PC.modules.faceWorking import faceDetector, globalFaceWorker
from PC.modules.imageWorking import decodeImage
from fastapi import FastAPI, Request
from traceback import format_exc
import uvicorn

detHands = handDetector(detectionCon=0.6, minTrackCon=0.6, maxHands=2)
detFaces = faceDetector(detectionCon=0.6, minTrackCon=0.6, maxFaces=1)
handWorker = globalHandWorker()
faceWorker = globalFaceWorker()

app = FastAPI()

@app.post('/img/get-tracking/hand/lines')
async def getTrackingHandLines(request: Request):
    imgString = await request.body()
    try:
        img = decodeImage(imgString)
        hands = detHands.findHands(img, flipType=False)
        return hands
    except Exception:
        return f'[ERROR]: {format_exc()}'

@app.post('/img/get-tracking/face/lines')
async def getTrackingFaceLines(request: Request):
    imgString = await request.body()
    try:
        img = decodeImage(imgString)
        faces = detFaces.findFaces(img)
        return faces
    except Exception:
        return f'[ERROR]: {format_exc()}'

@app.post('/img/get-gesture')
async def getGestureByImage(request: Request):
    imgString = await request.body()
    try:
        img = decodeImage(imgString)
        gestureType, gestureName = detHands.getGestureNameByImg(img)
        return dict(type=gestureType, name=gestureName)
    except Exception:
        return f'[ERROR]: {format_exc()}'

if __name__ == '__main__':
    uvicorn.run('mainServer:app', host='localhost', port=8080, reload=True, log_level='info', workers=10)

# Заметки
# - jpg отправляется быстрее
# - склеивать изображение, выводя настоящее
# - эффект появления первых 3-ех ближайших точек лица при приближении руки
# - объяснить работу методов соединений сервера с устройством
# - https://www.articleshub.net/2023/09/kak-sdelat-javascript-i-python-rabotat.html
# - https://habr.com/ru/companies/vk/articles/557232/