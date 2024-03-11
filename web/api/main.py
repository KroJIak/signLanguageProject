from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

webPath = os.path.join(os.path.dirname(__file__), '..')
sitePath = os.path.join(webPath, 'resource', 'v2')
webApp = FastAPI()
webApp.mount('/assets', StaticFiles(directory=sitePath), name='assets')

@webApp.get("/")
async def mainPage():
    indexHTMLPath = os.path.join(sitePath, 'index.html')
    return FileResponse(indexHTMLPath)