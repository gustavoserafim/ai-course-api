from pydantic import BaseModel, Field
from bson import ObjectId

from app.schemas.lesson import LessonResponse

class Lesson(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    course_id: ObjectId = Field(default_factory=ObjectId, alias="course_id")
    module_id: ObjectId = Field(default_factory=ObjectId, alias="module_id")
    name: str
    content: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    
    def to_response(self):
        data = {
            "id": str(self.id),
            "course_id": str(self.course_id),
            "module_id": str(self.module_id),
            "name": self.name,
            "content": self.content
        }
        return LessonResponse(**data)