import asyncio
from dotenv import dotenv_values

from fastapi import BackgroundTasks, FastAPI
from http.client import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from src.content import generate_content

config = dotenv_values(".env")

app = FastAPI()

client = AsyncIOMotorClient(config.get('MONGODB_URI'))
db = client.yduqs

async def save_generated_content(content: dict):
    print(">>> Saving content to database")
    print(f"save_generated_content > content: \n\n{content}")
    await db.content.insert_one(content)
    print(">>> Content saved")

@app.get("/")
async def index():
    return {
        "message": "Nothing to see here."
    }

@app.post("/generate")
async def generate(background_tasks: BackgroundTasks):
    try:
        kwargs = {
            "course": "Ciências da Computação",
            "subject": "Sistemas Operacionais",
            "topic": "Introdução ao Sistema Operacional",
            "subtopic": "Origens dos Sistemas Operacionais",
            "callback": save_generated_content
        }
        background_tasks.add_task(generate_content, **kwargs)
        return {
            "status": "task started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))