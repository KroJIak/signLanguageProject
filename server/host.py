from fastapi import FastAPI
import uvicorn

from service.api.main import serviceApp
from db.api.main import dbApp
from web.api.main import webApp

"""s.kdfmvlzdkfjbv;skmf vnwsvkjednf,.b .erbh
setg('haehtr;khgn;osiebnetgh'
     'strh;bjesrkjgthesighieirjg'
     'ethelrkbjprotjb;pkn'
     ''
     'thbr'
     ''classmethodetrh
)"""

app = FastAPI()
app.mount('/service/', serviceApp)
app.mount('/db/', dbApp)
app.mount('/', webApp)

if __name__ == '__main__':
    uvicorn.run('host:app', host='localhost', port=2468, workers=10)