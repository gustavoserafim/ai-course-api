import traceback
import app.llm.prompts as prompts
from app.llm.tela import request_text_generation
from app.models.course import Course

async def generate_outline(outline):
    try:
        prompt = await prompts.convert_outline_prompt(outline)
        print(f"PROMPT >>>>\n\n{prompt}")
        return await request_text_generation(prompt=prompt)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e

async def generate_content(
    course: Course,
    topic: str = "",
    subtopic: str = ""):

    assert course is not None, "exception:COURSE_REQUIDED"
    assert topic is not None, "exception:TOPIC_REQUIDED"
    assert subtopic is not None, "exception:SUBTOPIC_REQUIDED"

    try:
        prompt = await prompts.content_prompt(
            course=course,
            topic=topic,
            subtopic=subtopic)

        return await request_text_generation(
            prompt=prompt,
            max_new_tokens=2000,
            temperature=0.3,
            top_p=0.95,
            repetition_penalty=1.2)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e

async def generate_course_detail(course: Course):
    assert course is not None, "exception:COURSE_REQUIDED"
    try:
        prompt = await prompts.course_detail_prompt(
            course=course)

        return await request_text_generation(
            prompt=prompt,
            max_new_tokens=1000,
            temperature=0.3,
            top_p=0.95,
            repetition_penalty=1.2)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise e