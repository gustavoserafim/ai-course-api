import json
import re
import traceback

def handle_response_motor_a(response, output='json'):

    try:
        result = response.json()['result']['result']
        cleaned_result = re.sub(r"<s>\[INST\].*?\[/INST\]", "", result, flags=re.DOTALL)
        cleaned_result = re.sub(r"<\/s>", "", cleaned_result, flags=re.DOTALL)

        if output == 'json': 
            return json.loads(cleaned_result)
        return cleaned_result

    except Exception as e:
        print(f"An error occurred while processing response: {e}")
        traceback.print_exc()
        raise e

def handle_response_motor_b(response, output='json'):
    print(response.json())
    try:
        result = response.json()['generated_text']

        if output == 'json': 
            return json.loads(result)
        return result

    except Exception as e:
        print(f"An error occurred while processing response: {e}")
        traceback.print_exc()
        raise e

def handle_response_openai(response, output='json'):
    print(response.json())
    try:
        result = response.json()['choices'][0]['message']['content'].strip()

        if output == 'json': 
            return json.loads(result)
        return result

    except Exception as e:
        print(f"An error occurred while processing response: {e}")
        traceback.print_exc()
        raise e

def handle_response_gemini(response, output='json'):
    try:
        result = response.text
        cleaned_result = re.sub(r"(```json|```)", "", result, flags=re.DOTALL)

        if output == 'json': 
            return json.loads(cleaned_result)
        return cleaned_result

    except Exception as e:
        print(f"An error occurred while processing response: {e}")
        traceback.print_exc()
        raise e    
    