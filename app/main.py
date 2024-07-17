from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.api.endpoints import websocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.include_router(websocket.router, tags=["websockets"])

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://your-domain.com",
    "http://yduqs-poc-dev.us-east-1.elasticbeanstalk.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {
        "message": "Welcome to the YDUQS AI API!"
    }