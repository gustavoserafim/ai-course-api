from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Depends
from bson import ObjectId
from app.db.mongodb import get_collection
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentUpdate, ContentResponse

def convert_object_id(content: dict) -> dict:
    if '_id' in content:
        content['id'] = str(content['_id'])
        del content['_id']
    if 'course_id' in content:
        content['course_id'] = str(content['course_id'])
    return content


class ContentService:
    def __init__(self, collection: AsyncIOMotorCollection = Depends(lambda: get_collection("contents"))):
        if collection is None:
            raise ValueError("Collection dependency is None")
        self.collection = collection

    async def create_content(self, content_data: ContentCreate) -> ContentResponse:
        content_dict = content_data.dict()
        content_dict['course_id'] = ObjectId(content_dict['course_id'])
        result = await self.collection.insert_one(content_dict)
        content_dict['_id'] = result.inserted_id
        return ContentResponse(**convert_object_id(content_dict))

    async def list_content(self) -> List[ContentResponse]:
        contents = []
        async for content in self.collection.find():
            contents.append(ContentResponse(**convert_object_id(content)))
        return contents

    async def get_content(self, content_id: str) -> Optional[ContentResponse]:
        content = await self.collection.find_one({"_id": ObjectId(content_id)})
        if content:
            return ContentResponse(**convert_object_id(content))
        return None

    async def update_content(self, content_id: str, content_data: ContentUpdate) -> Optional[ContentResponse]:
        update_data = {
            "$set": {
                k: v for k, v in content_data.dict(exclude_unset=True).items() if v is not None
            }
        }
        updated_content = await self.collection.find_one_and_update({
            "_id": ObjectId(content_id)}, 
            update_data,
            return_document=True)
        return ContentResponse(**convert_object_id(updated_content))

    async def delete_content(self, content_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(content_id)})
        return result.deleted_count == 1