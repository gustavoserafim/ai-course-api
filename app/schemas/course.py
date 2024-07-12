from pydantic import BaseModel

class CourseBase(BaseModel):
    name: str
    description: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        fields = {'id': '_id'}
