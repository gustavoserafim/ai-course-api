from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.lesson import LessonCreate, LessonResponse, LessonUpdate
from app.services.lesson_service import LessonService


router = APIRouter()

@router.post("/", response_model=LessonResponse)
async def create_lesson(lesson: LessonCreate, service: LessonService = Depends()):
    lesson = await service.create_lesson(lesson)
    return lesson.to_response()

@router.get("/", response_model=List[LessonResponse])
async def get_lessons(service: LessonService = Depends()):
    lesson_list = await service.list_lesson()
    return [lesson.to_response() for lesson in lesson_list]

@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: str, service: LessonService = Depends()):
    lesson = await service.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson.to_response()

@router.patch("/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: str,
    lesson: LessonUpdate,
    service: LessonService = Depends()):
    lesson = await service.update_lesson(lesson_id, lesson)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson.to_response()

@router.delete("/{lesson_id}", response_model=None)
async def delete_lesson(lesson_id: str, service: LessonService = Depends()):
    success = await service.delete_lesson(lesson_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"detail": "Lesson deleted successfully"}