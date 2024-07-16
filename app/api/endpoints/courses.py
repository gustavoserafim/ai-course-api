import asyncio
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.models.course import Course
from app.schemas.content import ContentBlock, ContentCreate
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.services.content_service import ContentService
from app.services.course_service import CourseService

router = APIRouter()

@router.post("/", response_model=CourseResponse)
async def create_course(course: CourseCreate, service: CourseService = Depends()):
    return await service.create_course(course)

@router.get("/", response_model=List[CourseResponse])
async def get_courses(service: CourseService = Depends()):
    return await service.get_courses()

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
    return await service.update_course(course_id, course)

async def task_generate_content(
    course: Course,
    content_service: ContentService) -> None:

    await asyncio.sleep(5)

    content = ContentCreate(
        course_id=str(course.id),
        name="Generated Content",
        content=[
            ContentBlock(
                type="text", 
                content="This is a generated content block")
        ])

    await content_service.create_content(content)
    print("CONCLUIU A GERAÇÃO")

@router.post("/{course_id}/generate-content", response_model=None)
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