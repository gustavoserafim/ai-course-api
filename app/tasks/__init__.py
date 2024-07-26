import json
import time
import traceback
from app.models.course import Course
from app.models.module import Module
from app.schemas.course import CourseUpdate
from app.schemas.lesson import LessonCreate
from app.schemas.module import ModuleCreate
from app.services.lesson_service import LessonService
from app.llm.generator import (
  generate_course_detail, 
  generate_course_modules, 
  generate_module_lesson, 
)
from app.api.endpoints.websocket import manager as ws
from app.services.course_service import CourseService
from app.services.module_service import ModuleService

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def task_unified_generate_course(
    course: Course,
    course_service: CourseService,
    module_service: ModuleService,
    lesson_service: LessonService) -> None:

    print("START: task_unified_generate_course")
    start_time = time.time()

    with tracer.start_as_current_span("task_unified_generate_course") as span:
        span.set_attribute("Course", str(course.name))

        try:

            # update course status to READY
            course_status = CourseUpdate(**{
                "status": "PROCESSING"
            })
            await course_service.update_course(course.id, course_status)

            # generate course detail
            course_details = await generate_course_detail(course)
            details = CourseUpdate(**course_details.get("data"))
            await course_service.update_course(course.id, details)

            # generate course modules
            module_details = await generate_course_modules(course)

            for module in module_details.get("data"):
                module_dict = {
                    "course_id": str(course.id),
                    "name": module['name'],
                    "generated_objective": module['objective'],
                    "subtopics": module['subtopics']
                }
                new_module = ModuleCreate(**module_dict)
                module_created = await module_service.create_module(new_module)
            
                # generate lessons
                for lesson_name in new_module.subtopics:
                    content = await generate_module_lesson(
                        course_name=course.name,
                        module_name=module_created.name,
                        lesson_name=lesson_name)

                    lesson_data = {
                        "course_id": str(course.id),
                        "module_id": str(module_created.id),
                        "name": lesson_name,
                        "content": content
                    }

                    new_lesson = LessonCreate(**lesson_data)
                    await lesson_service.create_lesson(new_lesson)
            
            # update course status to READY
            course_status = CourseUpdate(**{
                "status": "READY"
            })
            await course_service.update_course(course.id, course_status)

            # notify the user that the course content was generated
            await ws.broadcast(json.dumps({
                "message": f'Content generation of course "{course.name}" completed',
                "status": "COMPLETED"
            }))
        except Exception as e:
            await ws.broadcast(json.dumps({
                "message": f'We had a problem to generate course content for "{course.name}"',
                "details": str(e),
                "status": "ERROR"
            }))
            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

    end_time = time.time()
    execution_time = end_time - start_time
    print("COMPLETED: task_unified_generate_course")
    print(f"Execution time: {execution_time:.2f}.")