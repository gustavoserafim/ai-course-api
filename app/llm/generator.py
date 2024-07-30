import traceback
import app.llm.prompts as prompts
from app.llm.tela import request_text_generation
from app.models.course import Course

from opentelemetry import trace

from app.models.tela_log import ContentTypeEnum
from app.schemas.tela_log import TelaLogCreate
from app.services.telalog_service import make_telalog_service

tracer = trace.get_tracer(__name__)

async def generate_course_detail(course: Course):
    assert course is not None, "exception:COURSE_REQUIDED"

    with tracer.start_as_current_span("generate_course_detail") as span:
        span.set_attribute("Course", str(course.name))

        try:
            tela_service = await make_telalog_service()

            prompt = await prompts.course_detail_prompt(
                course=course)

            response = await request_text_generation(
                prompt=prompt,
                max_new_tokens=1000,
                temperature=0.3,
                top_p=0.95,
                repetition_penalty=1.2)

            log = TelaLogCreate(
                content_type=ContentTypeEnum.COURSE,
                prompt=prompt,
                response=response,
                data={
                    "course_id": str(course.id)
                }
            )

            await tela_service.register_log(log)

            return response

        except Exception as e:
            span.set_status(trace.StatusCode.ERROR)
            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

async def generate_course_modules(course: Course):
    assert course is not None, "exception:COURSE_REQUIDED"
    try:
        tela_service = await make_telalog_service()

        prompt = await prompts.module_objectives_prompt(
            course=course)
        
        print(prompt)

        response =  await request_text_generation(
            prompt=prompt,
            max_new_tokens=1000,
            temperature=0.1,
            top_p=0.95,
            repetition_penalty=1.2)

        log = TelaLogCreate(
            content_type=ContentTypeEnum.MODULE,
            prompt=prompt,
            response=response,
                data={
                    "course_id": str(course.id)
                }
        )
        
        await tela_service.register_log(log)

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e

async def generate_module_lesson(
    course_name: str,
    module_name: str,
    lesson_name: str):
    
    assert all([
        course_name, 
        module_name, 
        lesson_name
    ]), "exception:COURSE_REQUIDED"

    try:
        tela_service = await make_telalog_service()

        prompt = await prompts.lesson_prompt(
            course_name, module_name, lesson_name)
        
        print(prompt)

        response = await request_text_generation(
            prompt=prompt,
            max_new_tokens=5000,
            temperature=0.1,
            top_p=0.95,
            repetition_penalty=1.2,
            output="text")

        log = TelaLogCreate(
            content_type=ContentTypeEnum.LESSON,
            prompt=prompt,
            response=response,
            data={
                "course_name": course_name
            }
        )
        
        await tela_service.register_log(log)

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e