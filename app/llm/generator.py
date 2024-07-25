import traceback
import app.llm.prompts as prompts
from app.llm.tela import request_text_generation
from app.models.course import Course

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def generate_course_detail(
        course: Course
):
    assert course is not None, "exception:COURSE_REQUIDED"

    with tracer.start_as_current_span("generate_course_detail") as span:
        span.set_attribute("Course", str(course.name))

        try:
            prompt = await prompts.course_detail_prompt(
                course=course)

            return await request_text_generation(
                prompt=prompt,
                max_new_tokens=1000,
                temperature=0.3,
                top_p=0.95,
                repetition_penalty=1.2)

        except Exception as e:
            span.set_status(trace.StatusCode.ERROR)
            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

async def generate_course_modules(course: Course):
    assert course is not None, "exception:COURSE_REQUIDED"
    try:
        prompt = await prompts.module_objectives_prompt(
            course=course)
        
        print(prompt)

        return await request_text_generation(
            prompt=prompt,
            max_new_tokens=1000,
            temperature=0.1,
            top_p=0.95,
            repetition_penalty=1.2)

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
        prompt = await prompts.lesson_prompt(
            course_name, module_name, lesson_name)
        
        print(prompt)

        return await request_text_generation(
            prompt=prompt,
            max_new_tokens=5000,
            temperature=0.1,
            top_p=0.95,
            repetition_penalty=1.2,
            output="text")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e