from typing import Optional
from pydantic import BaseModel

class CourseBase(BaseModel):
    name: str
    nature: Optional[str] = None
    faculty_profile: Optional[str] = None
    sylabus: Optional[str] = None
    objectives: Optional[str] = None
    learning_topics: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
