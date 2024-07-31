import traceback
import app.llm.prompts as prompts
from app.llm.tela import calculate_readability_metrics, request_text_generation
from app.models.course import Course

from opentelemetry import trace

from app.models.prompt_store import ContentTypeEnum
from app.schemas.prompt_store import PromptStoreCreate
from app.services.prompt_store_service import make_prompt_store_service

tracer = trace.get_tracer(__name__)

async def retryable_tela_request(prompt: prompts.Prompt, output='json', **kwargs) -> None:
    prompt_store_service = await make_prompt_store_service()

    while True:
        response = await request_text_generation(prompt, output)
        metrics = await calculate_readability_metrics(response)
        kwargs.update(metrics=str(metrics))

        print(kwargs)

        log = PromptStoreCreate(
            content_type=ContentTypeEnum.COURSE,
            prompt=prompt,
            response=response,
            data=kwargs)

        await prompt_store_service.register_log(log)

        if metrics == ('High', 'Normal', 'High'):
            break

    return response

async def generate_course_detail(course: Course):
    assert course is not None, "exception:COURSE_REQUIDED"

    with tracer.start_as_current_span("generate_course_detail") as span:
        span.set_attribute("Course", str(course.name))

        try:
            prompt = await prompts.course_detail_prompt(course=course)
            return await retryable_tela_request(prompt, course_id=str(course.id))
        except Exception as e:
            span.set_status(trace.StatusCode.ERROR)
            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

async def generate_course_modules(course: Course):
    assert course is not None, "exception:COURSE_REQUIDED"
    try:
        prompt = await prompts.module_objectives_prompt(course=course)
        return await retryable_tela_request(prompt, course_id=str(course.id))
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e

async def generate_module_lesson(
    course_id: str,
    course_name: str,
    module_name: str,
    lesson_name: str):
    
    assert all([
        course_id,
        course_name, 
        module_name, 
        lesson_name
    ]), "exception:COURSE_REQUIDED"

    try:
        prompt = await prompts.lesson_prompt(course_name, module_name, lesson_name)
        return await retryable_tela_request(prompt, course_id=str(course_id), output='text')
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e