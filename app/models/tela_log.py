import datetime
from enum import Enum
from typing import Dict, Optional, Union
from pydantic import BaseModel, Field
from bson import ObjectId

class ContentTypeEnum(str, Enum):
    COURSE = "COURSE"
    MODULE = "MODULE"
    LESSON = "LESSON"

class TelaLog(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id", description="Identificador único para o curso")
    content_type: ContentTypeEnum
    prompt: str
    response: Optional[Union[str, dict]] = None
    data: Optional[Dict[str, str]] = None
    created_at: datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True