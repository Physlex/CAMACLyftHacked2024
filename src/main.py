from fastapi import FastAPI
import uvicorn

from models import User

app = FastAPI()

### API

# @app.mount()
# @app.mount()
# @app.mount()

# def render():


## MAIN

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    pass
