from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.api.endpoints import websocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.websocket import manager as ws

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.include_router(websocket.router, tags=["websockets"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {
        "message": "Welcome to the YDUQS AI API!"
    }

@app.get("/ping")
async def ws_ping():
    await ws.broadcast("Pong!")
    return {
        "message": "Sending ping to all clients."
    }