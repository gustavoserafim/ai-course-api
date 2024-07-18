from fastapi import APIRouter

from . import content
from . import courses
from . import module

router = APIRouter()
router.include_router(courses.router, prefix="/course", tags=["courses"])
router.include_router(content.router, prefix="/content", tags=["contents"])
router.include_router(module.router, prefix="/module", tags=["contents"])
