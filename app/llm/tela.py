import json
import re
import traceback
import httpx
from app.core.config import settings

from opentelemetry import trace

from app.llm.prompts import Prompt

tracer = trace.get_tracer(__name__)

async def request_text_generation(
    prompt: Prompt,
    output: str='json'):

    with tracer.start_as_current_span("request_text_generation") as span:
        span.set_attribute("prompt", str(prompt.model_dump()))

        url = f"{settings.TELA_URL}/text-to-generate"

        headers = {
            "Content-Type": "application/json",
            "accept": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                with tracer.start_as_current_span("request_to_TELA_text_generation") as req_span:
                    response = await client.post(url, headers=headers, json=prompt.model_dump())
                    req_span.set_attribute("response_status_code", str(response))

                    # Cost metrics...
                    req_span.set_attribute("cost", str(response.json()['result']['cost']))
                    req_span.set_attribute("input_cost", str(response.json()['result']['input_cost']))
                    req_span.set_attribute("output_cost", str(response.json()['result']['output_cost']))
                    req_span.set_attribute("input_tokens_count", str(response.json()['result']['input_tokens_count']))
                    req_span.set_attribute("output_tokens_count", str(response.json()['result']['output_tokens_count']))
                    req_span.set_attribute("total_tokens_count", str(response.json()['result']['total_tokens_count']))
                    req_span.set_attribute("cost_per_token", str(response.json()['result']['cost']/response.json()['result']['total_tokens_count']))
                    
                    result = response.json()['result']['result']
                    req_span.set_attribute("result", str(result))
                    
                    cleaned_result = re.sub(r"<s>\[INST\].*?\[/INST\]", "", result, flags=re.DOTALL)
                    cleaned_result = re.sub(r"<\/s>", "", cleaned_result, flags=re.DOTALL)
                    req_span.set_attribute("cleaned_result", str(cleaned_result))

                    print(cleaned_result)

                    if output == 'json': 
                        result_ = json.loads(cleaned_result)
                    else:
                        result_ = cleaned_result

                    req_span.set_attribute("result_json", str(result_))
                    span.set_status(trace.StatusCode.OK)
                    return result_

        except Exception as e:
            span.set_status(trace.StatusCode.ERROR)

            print(f"An error occurred: {e}")
            traceback.print_exc()
            raise e

async def calculate_readability_metrics(text):
    import random
    responses = [
        ('High', 'Normal', 'High'), 
        ('High', 'Low', 'High')
    ]
    probabilities = [1/3, 2/3]
    return random.choices(responses, probabilities)[0]