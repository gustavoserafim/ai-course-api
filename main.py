import asyncio
from http.client import HTTPException
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

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
        return {
            "status": "task started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
