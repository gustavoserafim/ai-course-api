from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.tasks import task_generate_content
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.services.content_service import ContentService
from app.services.course_service import CourseService

router = APIRouter()

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
    course_service: CourseService = Depends(),
    content_service: ContentService = Depends()):

    print("STARTING GENERATION")
    course = await course_service.get_course(course_id)

    background_tasks.add_task(
        task_generate_content,
        course=course,
        content_service=content_service)

    return {"status": "Content generation started"}