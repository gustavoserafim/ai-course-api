import json
import app.llm.helpers as helpers
import app.llm.prompts as prompts
from gradio_client import Client
from app.core import config
from app.models.course import Course

def initialize_llm_client(model: str):
    try:
        client = Client(model)
        print("LLM client initialized")
        return client
    except Exception as e:
        if config.DEBUG:
            print(f"Error initializing client: {e}")
        return None

client = initialize_llm_client(config.LLM_MODEL)

async def generate_content(
    course: Course,
    image_quantity: int = 0, 
    has_video: bool = False,
    callback=None) -> None:

    assert course is not None, "exception:COURSE_REQUIDED"

    try:
        client = Client(config.LLM_MODEL)
        prompt = prompts.content_prompt(
            course=course,
            subject=subject,
            topic=topic,
            subtopic=subtopic,
            image_quantity=image_quantity,
            has_video=has_video
        )

        if config.DEBUG: helpers.input_stats("generate_content", prompt)

        response = client.predict(
            message=prompt,
            history="",
            temperature=0.3,
            max_new_tokens=10000,
            api_name='/predict')

        if len(response) > 0:
            if config.DEBUG: helpers.output_stats("generate_content", response)
            if callback:
                callback(json.loads(response))
            return json.loads(response)
        
        return {}

    except Exception as e:
        print(f"An error occurred: {e}")