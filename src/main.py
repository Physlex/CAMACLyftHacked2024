from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import uvicorn

from models import User

app = FastAPI()

### API

@app.mount("/templates", StaticFiles(directory="/templates"), name="/templates")
@app.mount("/static/css", StaticFiles(directory="/static/css"), name="/static/css")
@app.mount("/static/data", StaticFiles(directory="/static/data", name="/static/data"))
@app.mount("/static/js", StaticFiles(directory="/static/js"), name="/static/js")

@app.get("/", response_class=HTMLResponse)
async def index():
    pass

@app.get("/download")
async def download():
    """
        TODO: Takes a userID and returns it's associated streamed data
    """
    return JSONResponse([])


## MAIN

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    pass
