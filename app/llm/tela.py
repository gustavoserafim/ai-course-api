import traceback
from typing import Callable
import httpx
from app.core.config import settings

from opentelemetry import trace

from app.llm import prompts
from app.llm.handlers import handle_response_motor_a, handle_response_motor_b
from app.llm.models import MotorEnum, PROMPT_HANDLER_LIST

tracer = trace.get_tracer(__name__)

async def make_tela_request(
    url: str,
    headers: dict,
    payload: dict,
    output: str='json',
    span_name: str="request_to_TELA",
    response_handler=None):
    """
    Generic function to make requests to TELA API
    """

    with tracer.start_as_current_span(span_name) as span:
        span.set_attribute("url", url)
        span.set_attribute("payload", str(payload))

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                with tracer.start_as_current_span(f"{span_name}_http_request") as req_span:
                    response = await client.post(url, headers=headers, json=payload)
                    req_span.set_attribute("response_status_code", str(response.status_code))
                    if response_handler:
                        result = response_handler(response, output)
                    else:
                        result = response.json()
                    span.set_status(trace.StatusCode.OK)
                    return result
        except Exception as e:
            span.set_status(trace.StatusCode.ERROR)
            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

async def request_motor_a(prompt: prompts.PromptMotorA, output: str='json'):
    url = f"{settings.TELA_MOTOR_A_URL}/text-to-generate"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    payload = prompt.model_dump()

    return await make_tela_request(
        url=url,
        headers=headers,
        payload=payload,
        output=output,
        span_name="request_to_TELA_text_generation",
        response_handler=handle_response_motor_a)

async def request_motor_b(prompt: prompts.PromptMotorB, output: str='json'):
    url = f"{settings.TELA_MOTOR_B_URL}/generate"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    payload = prompt.model_dump()

    return await make_tela_request(
        url=url,
        headers=headers,
        payload=payload,
        output=output,
        span_name="request_to_TELA_generate",
        response_handler=handle_response_motor_b)


async def calculate_readability_metrics(text):
    import random
    responses = [
        ('High', 'Normal', 'High'), 
        ('High', 'Low', 'High')
    ]
    # probabilities = [1/3, 2/3]
    probabilities = [1, 0]
    return random.choices(responses, probabilities)[0]

async def tela_request_factory(
    motor: prompts.MotorEnum = prompts.MotorEnum.MOTOR_A) -> Callable:

    print(motor)

    match motor:
        case MotorEnum.MOTOR_A:
            return request_motor_a
        case MotorEnum.MOTOR_B:
            return request_motor_b
        case _:
            raise ValueError(f"Invalid motor: {motor}")