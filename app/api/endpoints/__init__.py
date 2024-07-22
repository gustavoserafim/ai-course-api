from fastapi import APIRouter

from . import content
from . import courses
from . import module

router = APIRouter()
router.include_router(courses.router, prefix="/courses", tags=["courses"])
router.include_router(content.router, prefix="/lessons", tags=["lessons"])
router.include_router(module.router, prefix="/modules", tags=["contents"])
