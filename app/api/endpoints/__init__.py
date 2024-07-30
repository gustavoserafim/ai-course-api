from fastapi import APIRouter

from . import lesson
from . import courses
from . import module
from . import prompt_store

router = APIRouter()
router.include_router(courses.router, prefix="/courses", tags=["courses"])
router.include_router(lesson.router, prefix="/lessons", tags=["lessons"])
router.include_router(module.router, prefix="/modules", tags=["modules"])
router.include_router(prompt_store.router, prefix="/prompt_stores", tags=["prompt_store"])
