import datetime
from enum import Enum
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field
from bson import ObjectId

from app.llm.models import PROMPT_HANDLER_LIST
from app.schemas.prompt_store import PromptStoreResponse

class ContentTypeEnum(str, Enum):
    COURSE = "COURSE"
    MODULE = "MODULE"
    LESSON = "LESSON"

class PromptStore(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    content_type: ContentTypeEnum
    prompt: PROMPT_HANDLER_LIST
    response: Optional[Union[str, dict]] = None
    data: Optional[Dict[str, str]] = None
    scores: Optional[Dict[str, Dict[str, Any]]] = None
    created_at: datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

    def to_response(self):
        data = {
            "id": str(self.id),
            "content_type": self.content_type,
            "prompt": self.prompt,
            "response": self.response,
            "data": self.data,
            "scores": self.scores,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }

        return PromptStoreResponse(**data)