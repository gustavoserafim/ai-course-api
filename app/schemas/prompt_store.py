import datetime
from typing import Dict, Optional, Union
from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.prompt_store import ContentTypeEnum


class PromptStoreBase(BaseModel):
    content_type: ContentTypeEnum
    prompt: str
    response: Optional[Union[str, dict]] = None
    data: Optional[Dict[str, str]] = None
    created_at: datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

class PromptStoreCreate(PromptStoreBase):
    pass