import datetime
from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.mongodb import get_collection
from app.models.prompt_store import PromptStore
from app.schemas.prompt_store import PromptStoreCreate


class PromptStoreService:
    def __init__(self, collection: AsyncIOMotorCollection):
        if collection is None:
            raise ValueError("Collection dependency is None")
        self.collection = collection

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