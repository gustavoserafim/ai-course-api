
import datetime
from typing import List
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from app.db.mongodb import get_collection
from app.models.tela_log import TelaLog
from app.schemas.tela_log import TelaLogCreate


class TelaLogService:
    def __init__(self, collection: AsyncIOMotorCollection):
        if collection is None:
            raise ValueError("Collection dependency is None")
        self.collection = collection

    async def register_log(self, data: TelaLogCreate) -> TelaLog:
        log_dict = data.dict()
        log_dict["created_at"] = datetime.datetime.utcnow()
        log_dict["updated_at"] = datetime.datetime.utcnow()
        result = await self.collection.insert_one(log_dict)
        log_dict['id'] = str(result.inserted_id)
        return TelaLog(**log_dict)

async def make_telalog_service() -> TelaLogService:
    collection = get_collection("prompt_store")
    return TelaLogService(collection=collection)