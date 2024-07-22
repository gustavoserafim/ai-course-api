from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Depends
from bson import ObjectId
from app.db.mongodb import get_collection
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonUpdate


class LessonService:
    def __init__(self, collection: AsyncIOMotorCollection = Depends(lambda: get_collection("lessons"))):
        if collection is None:
            raise ValueError("Collection dependency is None")
        self.collection = collection

    async def create_lesson(self, lesson_data: LessonCreate) -> Lesson:
        lesson_dict = lesson_data.dict()
        lesson_dict['course_id'] = ObjectId(lesson_dict['course_id'])
        lesson_dict['module_id'] = ObjectId(lesson_dict['module_id'])
        result = await self.collection.insert_one(lesson_dict)
        lesson_dict['_id'] = result.inserted_id
        print(lesson_dict)
        return Lesson(**lesson_dict)

    async def list_lesson(self, course_id: str = None, module_id: str = None) -> List[Lesson]:
        lessons = []
        query = {}
        if course_id:
            query['course_id'] = ObjectId(course_id)
        if module_id:
            query['module_id'] = ObjectId(module_id)
        async for lesson in self.collection.find(query):
            lessons.append(Lesson(**lesson))
        return lessons

    async def get_lesson(self, lesson_id: str) -> Optional[Lesson]:
        lesson = await self.collection.find_one({"_id": ObjectId(lesson_id)})
        if lesson:
            return Lesson(**lesson)
        return None

    async def update_lesson(self, lesson_id: str, lesson_data: LessonUpdate) -> Optional[Lesson]:
        update_data = {
            "$set": {
                k: v for k, v in lesson_data.dict(exclude_unset=True).items() if v is not None
            }
        }
        updated_lesson = await self.collection.find_one_and_update({
            "_id": ObjectId(lesson_id)}, 
            update_data,
            return_document=True)
        return Lesson(**updated_lesson)

    async def delete_lesson(self, lesson_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(lesson_id)})
        return result.deleted_count == 1