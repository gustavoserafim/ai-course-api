import json
import time
import traceback
from app.models.course import Course
from app.schemas.content import ContentCreate
from app.schemas.course import CourseUpdate
from app.schemas.module import ModuleCreate
from app.services.content_service import ContentService
from app.llm.generator import generate_course_detail, generate_course_modules, generate_outline, generate_content
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

async def task_generate_content(
    course: Course,
    content_service: ContentService
) -> None:
    start_time = time.time() 

    with tracer.start_as_current_span("task_generate_content") as span:
        span.set_attribute("Course", str(course.name))

        try:
            outline = await generate_outline(course.learning_topics)
            for section in outline.get('outline', []):
                topic = section.get('topic')
                subtopic_list = section.get('subtopics', [])
                for subtopic in subtopic_list:
                    print(f"GENERATE CONTENT FOR: {topic} > {subtopic}")
                    content = await generate_content(
                        course=course,
                        topic=topic,
                        subtopic=subtopic)
                    print(f"CONTENT >>>\n\n {content}")
                    await save_content(
                        course=course,
                        topic=topic, 
                        subtopic=subtopic, 
                        content=content.get('content_blocks'),
                        content_service=content_service)
            
            await ws.broadcast(json.dumps({
                "message": f'Content for "{course.name}" generation completed',
                "status": "COMPLETED"
            }))

            print("TASK COMPLETED")

        except Exception as e:
            await ws.broadcast(json.dumps({
                "message": f'We had a problem to generate content for "{course.name}"',
                "details": str(e),
                "status": "ERROR"
            }))
            print(f"An error occurred: {e}")
            traceback.print_exc()
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.2f}.")

async def save_content(
    course: Course,
    topic: str, 
    subtopic: str, 
    content: str,
    content_service: ContentService) -> None:

    try:
        content = ContentCreate(
            course_id=str(course.id),
            name=f"{topic} > {subtopic}",
            content=content
        )
        await content_service.create_content(content)
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
        for module, objective in course_details.get("data").items():

            await module_service.create_module(ModuleCreate(**{
                "course_id": course.id,
                "name": module,
                "generated_objective": objective
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