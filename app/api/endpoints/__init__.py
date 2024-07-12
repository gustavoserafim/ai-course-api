from fastapi import APIRouter
from . import courses

router = APIRouter()
router.include_router(courses.router, prefix="/courses", tags=["courses"])
