from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client.yduqs

def get_collection(collection_name: str):
    if db is None:
        raise ValueError("Database connection is not established")
    return db[collection_name]
