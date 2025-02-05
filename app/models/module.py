import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from app.schemas.module import ModuleResponse


class Module(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    course_id: ObjectId = Field(default_factory=ObjectId, alias="course_id")
    name: str = Field(description="Nome do módulo")
    generated_objective: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
      
    def to_response(self):
        data = {
            "id": str(self.id),
            "course_id": str(self.course_id),
            "name": self.name,
            "generated_objective": self.generated_objective,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
        return ModuleResponse(**data)