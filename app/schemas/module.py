from typing import Optional
from pydantic import BaseModel

class ModuleBase(BaseModel):
    course_id: str
    name: str
    generated_objective: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed=True

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(ModuleBase):
    name: Optional[str] = None
    course_id: Optional[str] = None

class ModuleResponse(ModuleBase):
    id: str
    course_id: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
