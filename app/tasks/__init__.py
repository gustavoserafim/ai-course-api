import json
import time
import traceback
from app.llm.models import MotorEnum
from app.models.course import Course
from app.models.module import Module
from app.schemas.course import CourseUpdate
from app.schemas.lesson import LessonCreate, LessonUpdate
from app.schemas.module import ModuleCreate
from app.services.lesson_service import LessonService
from app.llm.generator import (
    convert_outline_to_json,
    generate_course_detail,
    generate_lesson_video_script,
    generate_module_lesson,
    generate_module_objective,
)
from app.api.endpoints.websocket import manager as ws
from app.services.course_service import CourseService
from app.services.module_service import ModuleService

from opentelemetry import trace

from app.tasks import output

tracer = trace.get_tracer(__name__)


async def task_unified_generate_course(
    course: Course,
    course_service: CourseService,
    module_service: ModuleService,
    lesson_service: LessonService,
    motor: MotorEnum,
) -> None:
    print("START: task_unified_generate_course")
    start_time = time.time()

    with tracer.start_as_current_span("task_unified_generate_course") as span:
        span.set_attribute("Course", str(course.name))

        try:
            # update course status to READY
            course_status = CourseUpdate(**{"status": "PROCESSING"})
            await course_service.update_course(course.id, course_status)

            # generate outline structured
            outline_structured = await convert_outline_to_json(
                outline=course.learning_topics, motor=motor)
            
            print(outline_structured)

            await ws.broadcast(
                json.dumps(
                    {
                        "message": f'Generating course details',
                        "status": "PROCESSING",
                        "course_id": str(course.id)
                    }
                )
            )

            # generate course detail
            course_details = await generate_course_detail(course, motor=motor)
            details = CourseUpdate(**course_details.get("data"))
            await course_service.update_course(course.id, details)

            await ws.broadcast(
                json.dumps(
                    {
                        "message": f'Generating modules',
                        "status": "PROCESSING",
                        "course_id": str(course.id)
                    }
                )
            )

            total_lessons = sum(len(lesson) for lesson in outline_structured.values())
            lesson_count = 1
            for module_name in outline_structured.keys():
                module_lessons = outline_structured.get(module_name)
                generated_objective = await generate_module_objective(
                    course=course, 
                    module_name=module_name,
                    motor=motor)

                module_dict = {
                    "course_id": str(course.id),
                    "name": module_name,
                    "generated_objective": generated_objective,
                }
                new_module = ModuleCreate(**module_dict)
                module_created = await module_service.create_module(new_module)

                # generate lessons
                for lesson_name in module_lessons:
                    await ws.broadcast(
                        json.dumps(
                            {
                                "message": f'Generating lessons [{lesson_count}/{total_lessons}]',
                                "status": "PROCESSING",
                                "course_id": str(course.id)
                            }
                        )
                    )
                    content = await generate_module_lesson(
                        course_id = str(course.id),
                        learning_topics=course.learning_topics,
                        course_name=course.name,
                        module_name=module_created.name,
                        lesson_name=lesson_name,
                        motor=motor,
                    )

                    lesson_data = {
                        "course_id": str(course.id),
                        "module_id": str(module_created.id),
                        "name": lesson_name,
                        "content": content,
                    }

                    new_lesson = LessonCreate(**lesson_data)
                    lesson = await lesson_service.create_lesson(new_lesson)
                    lesson_count += 1

                    script = await generate_lesson_video_script(
                        course_id=str(course.id),
                        lesson_content = content,
                        motor=motor)
                    
                    await lesson_service.update_lesson(
                        lesson_id=lesson.id, 
                        lesson_data=LessonUpdate(**{"script": script}))

            # update course status to READY
            course_status = CourseUpdate(**{"status": "READY"})
            await course_service.update_course(course.id, course_status)

            # notify the user that the course content was generated
            await ws.broadcast(
                json.dumps(
                    {
                        "message": f'Content generation of course "{course.name}" completed',
                        "status": "COMPLETED",
                        "course_id": str(course.id)
                    }
                )
            )
        except Exception as e:
            await ws.broadcast(
                json.dumps(
                    {
                        "message": f'We had a problem to generate course content for "{course.name}"',
                        "details": str(e),
                        "status": "ERROR",
                        "course_id": str(course.id)
                    }
                )
            )
            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

    end_time = time.time()
    execution_time = end_time - start_time
    print("COMPLETED: task_unified_generate_course")
    print(f"Execution time: {execution_time:.2f}.")


async def task_generate_course_html(
    course_id: str,
    course_service: CourseService,
    module_service: ModuleService,
    lesson_service: LessonService,
) -> None:
    print("START: task_generate_course_html")
    start_time = time.time()

    try:
        context = {}

        course = await course_service.get_course(course_id)
        modules = await module_service.get_modules(course_id)
        lessons = await lesson_service.list_lesson(course_id)

        context["course"] = course.to_response()
        context["modules"] = [module.to_response() for module in modules]
        context["lessons"] = [lesson.to_response().dict() for lesson in lessons]

        html = output.to_html(context)

        # salvar no banco
        await course_service.update_course(course_id, CourseUpdate(**{"html": html}))

        await ws.broadcast(
            json.dumps(
                {
                    "message": f'HTML generation "{course.name}" completed',
                    "course_id": course_id,
                    "status": "COMPLETED",
                }
            )
        )
    except Exception as e:
        await ws.broadcast(
            json.dumps(
                {
                    "message": f'We had a problem to generate html for "{course.name}"',
                    "details": str(e),
                    "status": "ERROR",
                }
            )
        )
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e

    end_time = time.time()
    execution_time = end_time - start_time
    print("COMPLETED: task_generate_course_html")
    print(f"Execution time: {execution_time:.2f}.")
