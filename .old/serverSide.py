from PC.modules.imageWorking import *
from clientSide import getResultImage, getdbSize
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import uvicorn
import base64

app = FastAPI()

@app.post('/gestuno/img/')
async def getResult(request: Request):
    userByteData = await request.body()
    userData = eval(str(userByteData)[2:-1])
    imgBase64 = eval(f"""b'{userData["imageBase64"]}'""")
    imgString = base64.decodebytes(imgBase64[23:])
    mainImg = decodeImage(imgString)
    
    resultImg = getResultImage(mainImg, -1, linesHandThickness=2)

    imgBase64 = encodeImage2Base64(resultImg, format='png')
    return JSONResponse(content={"overlayImageBase64": imgBase64})


@app.get('/db/get-size')
async def getdbSize():
    return JSONResponse(content={"size": getdbSize()})


@app.options("/img/get-result")
async def optionsImage(): return

if __name__ == '__main__':
    uvicorn.run('serverSide:app', host='localhost', reload=True, port=8080, workers=10)