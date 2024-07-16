import asyncio
from app.models.course import Course
from app.schemas.content import ContentBlock, ContentCreate
from app.services.content_service import ContentService


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
