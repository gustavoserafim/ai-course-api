import datetime
from typing import List
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Depends
from bson import ObjectId
from app.db.mongodb import get_collection
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse

class CourseService:
    def __init__(self, collection: AsyncIOMotorCollection = Depends(lambda: get_collection("courses"))):
        if collection is None:
            raise ValueError("Collection dependency is None")
        self.collection = collection

    async def create_course(self, course_data: CourseCreate) -> CourseResponse:
        course_dict = course_data.dict()
        course_dict["created_at"] = datetime.datetime.utcnow()
        course_dict["updated_at"] = datetime.datetime.utcnow()
        result = await self.collection.insert_one(course_dict)
        course_dict['id'] = str(result.inserted_id)
        return Course(**course_dict)

    async def get_courses(self) -> List[CourseResponse]:
        courses = []
        async for course in self.collection.find():
            course['id'] = str(course['_id'])
            courses.append(Course(**course))
        return courses

    async def get_course(self, course_id: str) -> Course:
        course = await self.collection.find_one({"_id": ObjectId(course_id)})
        if course:
            return Course(**course)
        return None

    async def update_course(self, course_id: str, course_data: CourseUpdate) -> CourseResponse:
        course_dict = course_data.dict(exclude_unset=True)
        course_dict['updated_at'] = datetime.datetime.utcnow()
        update_data = {"$set": {k: v for k, v in course_dict.items() if v is not None}}
        await self.collection.update_one({"_id": ObjectId(course_id)}, update_data)
        updated_course = await self.collection.find_one({"_id": ObjectId(course_id)})
        updated_course['id'] = str(updated_course['_id'])
        return Course(**updated_course)