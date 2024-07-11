import asyncio
from dotenv import dotenv_values

from fastapi import BackgroundTasks, FastAPI
from http.client import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

config = dotenv_values(".env")


app = FastAPI()

client = AsyncIOMotorClient(config.get('MONGODB_URI'))
db = client.yduqs

async def simulate_delay(seconds: int):
    await asyncio.sleep(seconds)
    print("Delay complete")

@app.get("/")
async def index():
    return {
        "message": "Nothing to see here."
    }

@app.post("/generate")
async def generate(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(simulate_delay, 5)
        db.content.insert_one({"status": "task started"})
        return {
            "status": "task started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))