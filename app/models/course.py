from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from app.schemas.course import CourseResponse

class Course(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    nature: Optional[str] = None
    faculty_profile: Optional[str] = None
    sylabus: Optional[str] = None
    objectives: Optional[str] = None
    learning_topics: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
    
    def to_response(self):
        data = {
            "id": str(self.id),
            "name": self.name,
            "nature": self.nature,
            "faculty_profile": self.faculty_profile,
            "sylabus": self.sylabus,
            "objectives": self.objectives,
            "learning_topics": self.learning_topics
        }
        return CourseResponse(**data)