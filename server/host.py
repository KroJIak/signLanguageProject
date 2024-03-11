from fastapi import FastAPI
import uvicorn
from service.api.main import serviceApp
from db.api.main import dbApp
from web.api.main import webApp

app = FastAPI()
app.mount('/service/', serviceApp)
app.mount('/db/', dbApp)
app.mount('/', webApp)

if __name__ == '__main__':
    uvicorn.run('host:app', host='localhost', port=2468, workers=10)