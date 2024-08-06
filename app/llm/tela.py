import traceback
from typing import Callable
import httpx
from app.core.config import settings
import google.generativeai as genai

from opentelemetry import trace

from app.llm import prompts
from app.llm.handlers import handle_response_gemini, handle_response_motor_a, handle_response_motor_b, handle_response_openai
from app.llm.models import MotorEnum, PromptOpenAi

genai.configure(api_key=settings.GOOGLE_API_KEY)

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
        span_name="request_to_OPENAI_generate",
        response_handler=handle_response_motor_b)

async def request_openai(
    prompt: PromptOpenAi,
    output: str='json'):
    url = f"https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
    }

    payload = prompt.model_dump()

    return await make_tela_request(
        url=url,
        headers=headers,
        payload=payload,
        output=output,
        span_name="request_to_TELA_generate",
        response_handler=handle_response_openai)

async def request_gemini(prompt: str, output: str='json'):
    payload = prompt.model_dump()
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(payload.get('prompt'))
    print(response.text)
    return handle_response_gemini(response, output)

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

    match motor:
        case MotorEnum.MOTOR_A:
            return request_motor_a
        case MotorEnum.MOTOR_B:
            return request_motor_b
        case MotorEnum.OPEN_AI:
            return request_openai
        case MotorEnum.GEMINI:
            return request_gemini
        case _:
            raise ValueError(f"Invalid motor: {motor}")