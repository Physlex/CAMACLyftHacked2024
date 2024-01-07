from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import asyncio
import uvicorn

from models import User
from socketManager import SocketMan

from pathlib import Path
from serial import Serial

### GLOBALS

app = FastAPI()
server_socket = SocketMan()

### API

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/static/css", StaticFiles(directory="static/css"), name="static/css")
app.mount("/static/data", StaticFiles(directory="static/data"), name="static/data")
app.mount("/static/js", StaticFiles(directory="static/js"), name="static/js")

@app.get("/", response_class=HTMLResponse)
async def index():
    path = Path("templates/index.html")
    html: str = ""
    with open(path, 'r') as file:
        html = file.read()

    return HTMLResponse(html)

@app.get("/download")
async def download():
    """
        TODO: Takes a userID and returns it's associated streamed data
    """
    userID = 0
    new_user = User(userID)
    new_user.createUser()

    new_data = [0, 0, 1]
    new_user.upload(new_data)
    data = new_user.download()

    new_user.deleteUser()
    return JSONResponse(data)

@app.post("/authenticate")
async def authenticate(userID):
    return JSONResponse(True)

@app.websocket("/connect")
async def connect(websocket: WebSocket):
    print("work!")
    arduinoPort = "/dev/cu.usbmodem141401"

    await server_socket.connect(websocket)
    with Serial(device=arduinoPort) as serial_port:
        try:
            while True:
                await asyncio.sleep(0.1)
                await server_socket.send_acceleration(serial_port)
        except WebSocketDisconnect:
            await server_socket.disconnect()
    pass


## MAIN

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    pass
