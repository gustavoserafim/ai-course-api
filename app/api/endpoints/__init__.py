from fastapi import APIRouter

from . import content
from . import courses

router = APIRouter()
router.include_router(courses.router, prefix="/course", tags=["courses"])
router.include_router(content.router, prefix="/content", tags=["contents"])
