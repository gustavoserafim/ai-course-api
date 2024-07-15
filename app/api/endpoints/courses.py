from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
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
