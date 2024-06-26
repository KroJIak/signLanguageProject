from fastapi import FastAPI
import uvicorn

from service.api.main import serviceApp
from db.api.main import dbApp
from web.api.main import webApp
from server.modules.const import ConstPlenty

const = ConstPlenty()

app = FastAPI()
app.mount('/service/', serviceApp)
app.mount('/db/', dbApp)
app.mount('/', webApp)

if __name__ == '__main__':
    uvicorn.run('host:app', host='0.0.0.0', port=80, workers=1,
                ssl_keyfile=const.cert.keyfile,
                ssl_certfile=const.cert.certfile)