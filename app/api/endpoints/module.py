from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from app.schemas.module import ModuleCreate, ModuleResponse, ModuleUpdate
from app.services.course_service import CourseService
from app.services.lesson_service import LessonService
from app.services.module_service import ModuleService
from app.tasks import task_generate_module_lessons


router = APIRouter()

@router.post("/", response_model=ModuleResponse)
async def create_module(module: ModuleCreate, service: ModuleService = Depends()):
    module = await service.create_module(module)
    return module.to_response()

@router.get("/", response_model=List[ModuleResponse])
async def get_modules(
    course_id: Optional[str] = None, 
    service: ModuleService = Depends()):
    modules = await service.get_modules(course_id)
    return [module.to_response() for module in modules]

@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module(module_id: str, service: ModuleService = Depends()):
    module = await service.get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module.to_response()

@router.patch("/{module_id}", response_model=ModuleResponse)
async def update_module(
    module_id: str,
    module: ModuleUpdate,
    service: ModuleService = Depends()):
    module = await service.update_module(module_id, module)
    return module.to_response()

@router.delete("/{module_id}", response_model=None)
async def delete_module(module_id: str, service: ModuleService = Depends()):
    success = await service.delete_module(module_id)
    if not success:
        raise HTTPException(status_code=404, detail="Module not found")
    return {"detail": "Module deleted successfully"}

@router.post("/{module_id}/generate-lessons")
async def generate_course_modules(
    module_id: str,
    background_tasks: BackgroundTasks,
    module_service: ModuleService = Depends(),
    course_service: CourseService = Depends(),
    lesson_service: LessonService = Depends()):
    module = await module_service.get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    course = await course_service.get_course(str(module.course_id))
    background_tasks.add_task(
        task_generate_module_lessons,
        course = course,
        module=module,
        lesson_service=lesson_service)

    return {"status": "TASK_ENQUEUED"}