import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from app.schemas.course import CourseResponse


class CourseStatusEnum(str, Enum):
    DRAFT = "DRAFT"
    PROCESSING = "PROCESSING"
    READY = "READY"
    PEDAGOGIC_REVIEW = "PEDAGOGIC_REVIEW"
    QA_REVIEW = "QA_REVIEW"
    PUBLISHED = "PUBLISHED"

class Course(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id", description="Identificador único para o curso")
    name: str
    nature: Optional[str] = None
    semester_workload: Optional[int] = None
    weekly_workload: Optional[int] = None
    faculty_profile: Optional[str] = None
    thematic_area: Optional[str] = None
    extension_and_research_axis: Optional[str] = None
    competencies_to_be_developed: Optional[str] = None
    sylabus: Optional[str] = None
    objectives: Optional[str] = None
    socio_community_objectives: Optional[str] = None
    description_of_target_audience: Optional[str] = None
    justification: Optional[str] = None
    teaching_learning_procedures: Optional[str] = None
    learning_topics: Optional[str] = None
    assessment_procedures: Optional[str] = None
    basic_bibliography: Optional[str] = None
    complementary_bibliography: Optional[str] = None
    status: CourseStatusEnum = CourseStatusEnum.DRAFT
    generated_description: Optional[str] = None
    generated_propose: Optional[str] = None
    generated_introduction: Optional[str] = None
    generated_conclusion: Optional[str] = None
    html: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
    
    def to_response(self):
        data = {
            "id": str(self.id),
            "name": self.name,
            "nature": self.nature,
            "semester_workload": self.semester_workload,
            "weekly_workload": self.weekly_workload,
            "faculty_profile": self.faculty_profile,
            "thematic_area": self.thematic_area,
            "extension_and_research_axis": self.extension_and_research_axis,
            "competencies_to_be_developed": self.competencies_to_be_developed,
            "sylabus": self.sylabus,
            "objectives": self.objectives,
            "socio_community_objectives": self.socio_community_objectives,
            "description_of_target_audience": self.description_of_target_audience,
            "justification": self.justification,
            "teaching_learning_procedures": self.teaching_learning_procedures,
            "learning_topics": self.learning_topics,
            "assessment_procedures": self.assessment_procedures,
            "basic_bibliography": self.basic_bibliography,
            "complementary_bibliography": self.complementary_bibliography,
            "status": self.status,
            "generated_description": self.generated_description,
            "generated_propose": self.generated_propose,
            "generated_introduction": self.generated_introduction,
            "generated_conclusion": self.generated_conclusion,
            "html": self.html,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
        return CourseResponse(**data)