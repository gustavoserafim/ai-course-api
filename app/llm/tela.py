import json
import re
import traceback
import httpx
from app.core.config import settings

async def request_text_generation(
    prompt,
    max_new_tokens=2000,
    temperature=0.1,
    top_p=0.95,
    repetition_penalty=1.2):

    url = f"{settings.TELA_URL}/text-to-generate"

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

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

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(url, headers=headers, json=data)
            result = response.json()['result']['result']
            cleaned_result = re.sub(r"<s>\[INST\].*?\[/INST\]", "", result, flags=re.DOTALL)
            cleaned_result = re.sub(r"<\/s>", "", cleaned_result, flags=re.DOTALL)
            result_json = json.loads(cleaned_result)
            return result_json
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e