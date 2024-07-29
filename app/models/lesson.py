import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

from app.schemas.lesson import LessonResponse

class Lesson(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    course_id: ObjectId = Field(default_factory=ObjectId, alias="course_id")
    module_id: ObjectId = Field(default_factory=ObjectId, alias="module_id")
    name: str
    content: str
    created_at: datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    
    def to_response(self):
        data = {
            "id": str(self.id),
            "course_id": str(self.course_id),
            "module_id": str(self.module_id),
            "name": self.name,
            "content": self.content,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
        return LessonResponse(**data)