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
  generate_outline, 
  generate_lesson
)
from app.api.endpoints.websocket import manager as ws
from app.services.course_service import CourseService
from app.services.module_service import ModuleService

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def task_generate_course_detail(
    course: Course,
    course_service: CourseService
) -> None:
    with tracer.start_as_current_span("task_generate_course_detail") as span:
        span.set_attribute("Course", str(course.name))

        print("START: task_generate_course_detail")

        start_time = time.time() 
        try:
            course_details = await generate_course_detail(course)
            details = CourseUpdate(**course_details.get("data"))
            await course_service.update_course(course.id, details)
            await ws.broadcast(json.dumps({
                "message": f'Details for course "{course.name}" generated',
                "status": "COMPLETED"
            }))
        except Exception as e:
            await ws.broadcast(json.dumps({
                "message": f'We had a problem to generate details for "{course.name}"',
                "details": str(e),
                "status": "ERROR"
            }))
            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

        end_time = time.time()
        execution_time = end_time - start_time
        print("COMPLETED: task_generate_course_detail")
        print(f"Execution time: {execution_time:.2f}.")

async def task_generate_lesson(
    course: Course,
    lesson_service: LessonService
) -> None:
    start_time = time.time() 

    with tracer.start_as_current_span("task_generate_lesson") as span:
        span.set_attribute("Course", str(course.name))

        try:
            outline = await generate_outline(course.learning_topics)
            for section in outline.get('outline', []):
                topic = section.get('topic')
                subtopic_list = section.get('subtopics', [])
                for subtopic in subtopic_list:
                    print(f"GENERATE CONTENT FOR: {topic} > {subtopic}")
                    lesson = await generate_lesson(
                        course=course,
                        topic=topic,
                        subtopic=subtopic)
                    print(f"CONTENT >>>\n\n {lesson}")
                    await save_lesson(
                        course=course,
                        topic=topic, 
                        subtopic=subtopic, 
                        lesson=lesson.get('lesson_blocks'),
                        lesson_service=lesson_service)
            
            await ws.broadcast(json.dumps({
                "message": f'Lesson for "{course.name}" generation completed',
                "status": "COMPLETED"
            }))

            print("TASK COMPLETED")

        except Exception as e:
            await ws.broadcast(json.dumps({
                "message": f'We had a problem to generate lesson for "{course.name}"',
                "details": str(e),
                "status": "ERROR"
            }))
            print(f"An error occurred: {e}")
            traceback.print_exc()
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.2f}.")

async def save_lesson(
    course: Course,
    topic: str, 
    subtopic: str, 
    lesson: str,
    lesson_service: LessonService) -> None:

    try:
        lesson = LessonCreate(
            course_id=str(course.id),
            name=f"{topic} > {subtopic}",
            lesson=lesson
        )
        await lesson_service.create_lesson(lesson)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e

async def task_generate_course_modules(
    course: Course,
    module_service: ModuleService) -> None:
    print("START: task_generate_course_modules")

    start_time = time.time() 
    try:
        course_details = await generate_course_modules(course)
        for module in course_details.get("data"):
            await module_service.create_module(ModuleCreate(**{
                "course_id": str(course.id),
                "name": module['name'],
                "generated_objective": module['objective'],
                "subtopics": module['subtopics']
            }))

        await ws.broadcast(json.dumps({
            "message": f'Modules of course "{course.name}" generated',
            "status": "COMPLETED"
        }))
    except Exception as e:
        await ws.broadcast(json.dumps({
            "message": f'We had a problem to generate modules for course "{course.name}"',
            "details": str(e),
            "status": "ERROR"
        }))
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e

    end_time = time.time()
    execution_time = end_time - start_time
    print("COMPLETED: task_generate_course_modules")
    print(f"Execution time: {execution_time:.2f}.")

async def task_generate_module_lessons(
    course: Course, 
    module: Module,
    lesson_service: LessonService) -> None:
    print("START: task_generate_module_lessons")

    start_time = time.time()
    try:
        for lesson_name in module.subtopics:
            content = await generate_module_lesson(
                course_name=course.name,
                module_name=module.name,
                lesson_name=lesson_name)
            
            print(content)

            await lesson_service.create_lesson(LessonCreate(**{
                "course_id": str(course.id),
                "module_id": str(module.id),
                "name": lesson_name,
                "content": content
            }))

        await ws.broadcast(json.dumps({
            "message": f'Lessons of module "{module.name}" generated',
            "status": "COMPLETED"
        }))
    except Exception as e:
        await ws.broadcast(json.dumps({
            "message": f'We had a problem to generate lessons of module "{module.name}"',
            "details": str(e),
            "status": "ERROR"
        }))
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e

    end_time = time.time()
    execution_time = end_time - start_time
    print("COMPLETED: task_generate_module_lessons")
    print(f"Execution time: {execution_time:.2f}.")