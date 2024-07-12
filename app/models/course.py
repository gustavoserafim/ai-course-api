from pydantic import BaseModel, Field
from bson import ObjectId

class Course(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    description: str

    class Config:
        arbitrary_types_allowed = True