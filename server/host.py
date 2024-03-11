from fastapi import FastAPI
import uvicorn
from service.api.main import serviceApp
from db.api.main import dbApp

app = FastAPI()
app.mount("/service/", serviceApp)
app.mount("/db/", dbApp)

if __name__ == '__main__':
    uvicorn.run('host:app', host='localhost', port=2468, workers=10)