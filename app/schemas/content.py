from typing import List, Optional, Dict, Any
from bson import ObjectId
from pydantic import BaseModel, Field

class ContentBase(BaseModel):
    course_id: str
    module_id: str
    name: str
    content: str

class ContentCreate(ContentBase):
    pass

class ContentUpdate(ContentBase):
    course_id: Optional[str] = None
    module_id: Optional[str] = None
    name: Optional[str] = None
    content: Optional[str] = None

class ContentResponse(ContentBase):
    id: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}