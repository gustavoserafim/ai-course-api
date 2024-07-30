import datetime
from typing import List
from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.mongodb import get_collection
from app.models.prompt_store import PromptStore
from app.schemas.prompt_store import PromptStoreCreate


class PromptStoreService:
    def __init__(self, collection: AsyncIOMotorCollection = Depends(lambda: get_collection("prompt_store"))):
        if collection is None:
            raise ValueError("Collection dependency is None")
        self.collection = collection

    async def list_prompt_store(self) -> List[PromptStore]:
        log_list = []
        async for log in self.collection.find().sort("created_at", -1):
            log['id'] = str(log['_id'])
            log_list.append(PromptStore(**log))
        return log_list

    async def get_prompt_store(self, prompt_store_id: str) -> PromptStore:
        log = await self.collection.find_one({"_id": ObjectId(prompt_store_id)})
        if log:
            return PromptStore(**log)
        return None

    async def register_log(self, data: PromptStoreCreate) -> PromptStore:
        log_dict = data.dict()
        log_dict["created_at"] = datetime.datetime.utcnow()
        log_dict["updated_at"] = datetime.datetime.utcnow()
        result = await self.collection.insert_one(log_dict)
        log_dict['id'] = str(result.inserted_id)
        return PromptStore(**log_dict)

async def make_prompt_store_service() -> PromptStoreService:
    collection = get_collection("prompt_store")
    return PromptStoreService(collection=collection)