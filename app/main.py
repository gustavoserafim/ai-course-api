from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI()
app.include_router(api_router, prefix="/api")

@app.get("/")
def index():
    return {
        "message": "Welcome to the YDUQS AI API!"
    }