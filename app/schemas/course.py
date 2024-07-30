from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class CourseStatusEnum(str, Enum):
    DRAFT = "DRAFT"
    PROCESSING = "PROCESSING"
    READY = "READY"
    PEDAGOGIC_REVIEW = "PEDAGOGIC_REVIEW"
    QA_REVIEW = "QA_REVIEW"
    PUBLISHED = "PUBLISHED"

class CourseBase(BaseModel):
    name: str = Field(..., description="Nome do curso")
    nature: Optional[str] = Field(None, description="Natureza do curso")
    semester_workload: Optional[int] = Field(None, description="Carga horária semestral em horas")
    weekly_workload: Optional[int] = Field(None, description="Carga horária semanal em horas")
    faculty_profile: Optional[str] = Field(None, description="Perfil do docente responsável pelo curso")
    thematic_area: Optional[str] = Field(None, description="Área temática do curso")
    extension_and_research_axis: Optional[str] = Field(None, description="Linha eixo de extensão e pesquisa")
    competencies_to_be_developed: Optional[str] = Field(None, description="Competências a serem trabalhadas durante o curso")
    sylabus: Optional[str] = Field(None, description="Ementa do curso")
    objectives: Optional[str] = Field(None, description="Objetivos do curso")
    socio_community_objectives: Optional[str] = Field(None, description="Objetivos sociocomunitários do curso")
    description_of_target_audience: Optional[str] = Field(None, description="Descrição do público envolvido")
    justification: Optional[str] = Field(None, description="Justificativa para o curso")
    teaching_learning_procedures: Optional[str] = Field(None, description="Procedimentos de ensino-aprendizagem")
    learning_topics: Optional[str] = Field(None, description="Temas de aprendizagem abordados no curso")
    assessment_procedures: Optional[str] = Field(None, description="Procedimentos de avaliação")
    basic_bibliography: Optional[str] = Field(None, description="Bibliografia básica do curso")
    complementary_bibliography: Optional[str] = Field(None, description="Bibliografia complementar do curso")
    status: Optional[CourseStatusEnum] = Field(CourseStatusEnum.DRAFT, description="Status do curso")
    generated_description: Optional[str] = None
    generated_propose: Optional[str] = None
    generated_introduction: Optional[str] = None
    generated_conclusion: Optional[str] = None
    html: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    name: Optional[str] = None

class CourseResponse(CourseBase):
    id: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
