from typing import List, Optional, Dict, Any
from bson import ObjectId
from pydantic import BaseModel, Field

class ContentBlock(BaseModel):
    type: str
    content: Optional[str] = None

class ContentData(BaseModel):
    content: List[ContentBlock]

class Content(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    course_id: ObjectId
    name: str
    content: List[ContentBlock]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ContentBase(BaseModel):
    course_id: str
    name: str
    content: List[ContentBlock]

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[ContentData] = None

class ContentResponse(ContentBase):
    id: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}