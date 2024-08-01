import datetime
from enum import Enum
from typing import Dict, Optional, Union
from bson import ObjectId
from pydantic import BaseModel, Field

from app.llm.models import PROMPT_HANDLER_LIST

class ContentTypeEnum(str, Enum):
    COURSE = "COURSE"
    MODULE = "MODULE"
    LESSON = "LESSON"

class PromptStoreBase(BaseModel):
    content_type: ContentTypeEnum
    prompt: PROMPT_HANDLER_LIST
    response: Optional[Union[str, dict]] = None
    data: Optional[Dict[str, str]] = None
    created_at: datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

class PromptStoreCreate(PromptStoreBase):
    pass

class PromptStoreResponse(PromptStoreBase):
    id: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class PromptStoreListParams(BaseModel):
    page: int = 1
    page_size: int = 20
    sort_by: str = "created_at"
