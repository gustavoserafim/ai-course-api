import json
import src.helpers as helpers
import src.prompts as prompts
from gradio_client import Client

from dotenv import dotenv_values

config = dotenv_values(".env")

DEBUG = config.get("DEBUG", False)
LLM_MODEL = config.get('LLM_MODEL')

def initialize_llm_client(model: str):
    try:
        client = Client(model)
        print("LLM client initialized")
        return client
    except Exception as e:
        if DEBUG:
            print(f"Error initializing client: {e}")
        return None

client = initialize_llm_client(LLM_MODEL)

def generate_course(course: str, subject: str) -> dict:
    """
    This prompt generate a course structure based on 
    the course and subject.
    """
    assert course is not None, "exception:COURSE_NAME_REQUIDED"
    assert subject is not None, "exception:SUBJECT_NAME_REQUIDED"

    try:
        prompt = prompts.course_prompt(course, subject)
        if DEBUG: helpers.input_stats("generate_course", prompt)

        response = client.predict(
            message=prompt,
            history="",
            temperature=0.1,
            max_new_tokens=10000,
            api_name='/predict')
        
        if len(response) > 0:
            print("ENTROU AQUI")
            if DEBUG: helpers.output_stats("generate_course", response)
            return json.loads(response)
        return {}

    except Exception as e:
        print(f"An error occurred: {e}")


def generate_outline(
    course: str,
    subject: str,
    chapter: str) -> dict:
    """
    This prompt generate an outline for a chapter
    """
    assert course is not None, "exception:COURSE_NAME_REQUIDED"
    assert subject is not None, "exception:SUBJECT_NAME_REQUIDED"
    assert chapter is not None, "exception:CHAPTER_NAME_REQUIDED"

    try:
      client = Client(LLM_MODEL)
      prompt = prompts.outline_prompt(course, subject, chapter)

      if DEBUG: helpers.input_stats("generate_outline", prompt)

      response = client.predict(
          message=prompt,
          history="",
          temperature=0.1,
          max_new_tokens=10000,
          api_name='/predict')
      

      if len(response) > 0:
          if DEBUG: helpers.output_stats("generate_outline", response)
          return json.loads(response)

      return {}

    except Exception as e:
        print(f"An error occurred: {e}")

async def generate_content(
    course: str,
    subject: str,
    topic: dict, 
    subtopic: str,
    image_quantity: int = 0, 
    has_video: bool = False,
    callback=None) -> None:

    assert course is not None, "exception:COURSE_NAME_REQUIDED"
    assert subject is not None, "exception:SUBJECT_NAME_REQUIDED"
    assert topic is not None, "exception:TOPIC_NAME_REQUIDED"
    assert subtopic is not None, "exception:SUBTOPIC_NAME_REQUID"

    try:
        client = Client(LLM_MODEL)
        prompt = prompts.content_prompt(
            course=course,
            subject=subject,
            topic=topic,
            subtopic=subtopic,
            image_quantity=image_quantity,
            has_video=has_video
        )

        if DEBUG: helpers.input_stats("generate_content", prompt)

        response = client.predict(
            message=prompt,
            history="",
            temperature=0.2,
            max_new_tokens=10000,
            api_name='/predict')

        if len(response) > 0:
            if DEBUG: helpers.output_stats("generate_content", response)
            if callback:
                callback(json.loads(response))
            return json.loads(response)
        
        return {}

    except Exception as e:
        print(f"An error occurred: {e}")