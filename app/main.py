from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.api.endpoints import websocket

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.include_router(websocket.router, tags=["websockets"])

@app.get("/")
def index():
    return {
        "message": "Welcome to the YDUQS AI API!"
    }