from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from app.services.module_service import ModuleService
from app.tasks import (
  task_generate_course_html,
  task_unified_generate_course
)
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate, GenerateContentPayload
from app.services.lesson_service import LessonService, LessonService
from app.services.course_service import CourseService

from opentelemetry import trace

router = APIRouter()

tracer = trace.get_tracer(__name__)

@router.post("/", response_model=CourseResponse)
async def create_course(course: CourseCreate, service: CourseService = Depends()):
    course = await service.create_course(course)
    return course.to_response()

@router.get("/", response_model=List[CourseResponse])
async def get_courses(service: CourseService = Depends()):
    courses = await service.get_courses()
    return [course.to_response() for course in courses]

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str, service: CourseService = Depends()):
    course = await service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.to_response()

@router.patch("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course: CourseUpdate,
    service: CourseService = Depends()):
    course = await service.update_course(course_id, course)
    return course.to_response()

@router.post("/{course_id}/generate-content")
async def generate_content(
    course_id: str,
    background_tasks: BackgroundTasks,
    payload: Optional[GenerateContentPayload] = Body(default=None),
    course_service: CourseService = Depends(),
    module_service: ModuleService = Depends(),
    lesson_service: LessonService = Depends()):

    with tracer.start_as_current_span("generate_content") as span:
        span.set_attribute("course_id", str(course_id))

        print("STARTING GENERATION")
        course = await course_service.get_course(course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        if payload is None:
            payload = GenerateContentPayload()

        span.set_attribute("motor", payload.model_dump())

        background_tasks.add_task(
            task_unified_generate_course,
            course=course,
            course_service=course_service,
            module_service=module_service,
            lesson_service=lesson_service,
            motor=payload.motor)

        return {"status": "TASK_ENQUEUED"}

@router.post("/{course_id}/generate-html")
async def generate_html(
    course_id: str,
    background_tasks: BackgroundTasks,
    course_service: CourseService = Depends(),
    module_service: ModuleService = Depends(),
    lesson_service: LessonService = Depends()):

    with tracer.start_as_current_span("generate_html") as span:
        span.set_attribute("course_id", str(course_id))

        background_tasks.add_task(
            task_generate_course_html,
            course_id=course_id,
            course_service=course_service,
            module_service=module_service,
            lesson_service=lesson_service)

        return {"status": "TASK_ENQUEUED"}