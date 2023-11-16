from ModuleImageWorking import decodeImage, encodeImage
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import numpy as np
import base64
import cv2

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def mainPage():
    return FileResponse("static/index.html")

@app.post('/img/get-test')
async def getTest(request: Request):
    imgBase64 = await request.body()
    imgString = base64.decodebytes(imgBase64[23:])
    mainImg = decodeImage(imgString)
    mainImg = cv2.flip(mainImg, 2)

    cv2.imshow('Image', mainImg)
    cv2.waitKey(1)
    imgString = encodeImage(mainImg)
    return Response(imgString)

@app.options("/img/get-test")
async def options_image(): return

if __name__ == '__main__':
    uvicorn.run('web.server:app', host='0.0.0.0', port=8080, reload=True, log_level='info')

# Заметки
# - jpg отправляется быстрее
# - склеивать изображение, выводя настоящее
# - эффект появления первых 3-ех ближайших точек лица при приближении руки
# - объяснить работу методов соединений сервера с устройством
# - https://www.articleshub.net/2023/09/kak-sdelat-javascript-i-python-rabotat.html