import traceback
from typing import Any
from app.llm import models
from app.llm.models import MotorEnum
from app.llm import prompts
from app.llm.tela import calculate_readability_metrics, tela_request_factory
from app.models.course import Course

from opentelemetry import trace

from app.models.prompt_store import ContentTypeEnum
from app.schemas.prompt_store import PromptStoreCreate
from app.services.prompt_store_service import make_prompt_store_service

tracer = trace.get_tracer(__name__)

async def retryable_tela_request(
    prompt: models.PROMPT_HANDLER_LIST, 
    motor: MotorEnum = MotorEnum.MOTOR_A,
    output='json',
    **kwargs) -> None:

    prompt_store_service = await make_prompt_store_service()

    tela_request_generation = await tela_request_factory(motor)

    while True:
        response = await tela_request_generation(prompt, output)
        metrics = await calculate_readability_metrics(response)
        kwargs.update(metrics=str(metrics))

        log = PromptStoreCreate(
            content_type=ContentTypeEnum.COURSE,
            prompt=prompt,
            response=str(response),
            data=kwargs)

        await prompt_store_service.register_log(log)

        if metrics == ('High', 'Normal', 'High'):
            break

    return response

async def convert_outline_to_json(
    outline: str,
    motor: MotorEnum = MotorEnum.MOTOR_A
) -> str:
    assert outline is not None, "exception:OUTLINE_REQUIDED"

    with tracer.start_as_current_span("generate_course_detail") as span:
        try:
            prompt_store_service = await make_prompt_store_service()
            tela_request_generation = await tela_request_factory(motor)

            prompt = await prompts.convert_outline_prompt(outline, motor=motor)
            response = await tela_request_generation(prompt)
            print(response)

            log = PromptStoreCreate(
                content_type=ContentTypeEnum.COURSE,
                prompt=prompt,
                response=str(response),
                data={
                    "outline": outline
                }
            )

            await prompt_store_service.register_log(log)
            return response

        except Exception as e:
            span.set_status(trace.StatusCode.ERROR)
            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

async def generate_course_detail(
    course: Course,
    motor: MotorEnum = MotorEnum.MOTOR_A) -> str:

    assert course is not None, "exception:COURSE_REQUIDED"

    with tracer.start_as_current_span("generate_course_detail") as span:
        span.set_attribute("Course", str(course.name))
        span.set_attribute("motor", str(motor))

        try:
            prompt = await prompts.course_detail_prompt(course=course, motor=motor)
            content = await retryable_tela_request(prompt, motor, course_id=str(course.id))
            print(content)
            return content
        except Exception as e:
            span.set_status(trace.StatusCode.ERROR)
            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

async def generate_course_modules(
    course: Course, 
    motor: MotorEnum = MotorEnum.MOTOR_A) -> str:

    assert course is not None, "exception:COURSE_REQUIDED"
    try:
        prompt_store_service = await make_prompt_store_service()
        tela_request_generation = await tela_request_factory(motor)

        prompt = await prompts.module_objectives_prompt(course=course, motor=motor)
        response = await tela_request_generation(prompt)
        print(response)

        log = PromptStoreCreate(
            content_type=ContentTypeEnum.COURSE,
            prompt=prompt,
            response=str(response),
            data={
                "course_id": str(course.id)
            }
        )
        await prompt_store_service.register_log(log)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e

async def generate_module_lesson(
    course_id: str,
    course_name: str,
    module_name: str,
    lesson_name: str,
    motor: MotorEnum = MotorEnum.MOTOR_A) -> str:
    
    assert all([
        course_id,
        course_name, 
        module_name, 
        lesson_name
    ]), "exception:COURSE_REQUIDED"

    try:
        prompt = await prompts.lesson_prompt(course_name, module_name, lesson_name, motor=motor)
        return await retryable_tela_request(prompt, motor, course_id=str(course_id), output='text')
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e