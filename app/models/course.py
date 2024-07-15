from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

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