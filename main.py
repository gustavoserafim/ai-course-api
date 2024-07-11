from http.client import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import asyncio

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    age: int

users = []

async def simulate_delay(seconds: int):
    await asyncio.sleep(seconds)

@app.get("/")
async def index():
    return {
        "message": "Nothing to see here."
    }


@app.get("/users", response_model=List[User])
async def get_users():
    try:
        await simulate_delay(1)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users", response_model=User)
async def create_user(user: User):
    try:
        await simulate_delay(1)
        users.append(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
