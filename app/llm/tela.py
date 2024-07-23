import json
import re
import traceback
import httpx
from app.core.config import settings

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def request_text_generation(
    prompt,
    max_new_tokens=2000,
    temperature=0.1,
    top_p=0.95,
    repetition_penalty=1.2,
    output='json'):

    with tracer.start_as_current_span("request_text_generation") as span:
        span.set_attribute("prompt", str(prompt))
        span.set_attribute("max_new_tokens", str(max_new_tokens))
        span.set_attribute("temperature", str(temperature))
        span.set_attribute("top_p", str(top_p))
        span.set_attribute("repetition_penalty", str(repetition_penalty))

        url = f"{settings.TELA_URL}/text-to-generate"

        span.set_attribute("url", str(url))

        headers = {
            "Content-Type": "application/json",
            "accept": "application/json"
        }

        span.set_attribute("headers", str(headers))

        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "repetition_penalty": repetition_penalty
        }

        span.set_attribute("data", str(data))

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                with tracer.start_as_current_span("request_to_TELA_text_generation") as req_span:
                    response = await client.post(url, headers=headers, json=data)
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