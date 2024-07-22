from typing import Optional
from pydantic import BaseModel

class LessonBase(BaseModel):
    course_id: str
    module_id: str
    name: str
    content: str

    class Config:
        arbitrary_types_allowed=True

class LessonCreate(LessonBase):
    pass

class LessonUpdate(LessonBase):
    course_id: Optional[str] = None
    module_id: Optional[str] = None
    name: Optional[str] = None
    content: Optional[str] = None

class LessonResponse(LessonBase):
    id: str

    class Config:
        arbitrary_types_allowed = True