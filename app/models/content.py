from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class Content(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    course_id: ObjectId
    module_id: ObjectId
    name: str
    content: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}