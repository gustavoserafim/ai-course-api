import json
from typing import Awaitable, Union

from opentelemetry import trace

from app.models.course import Course
from app.llm.models import (
    PROMPT_HANDLER_LIST,
    MotorEnum,
    PromptMotorA,
    PromptMotorB,
    prompt_handler_factory,
)

tracer = trace.get_tracer(__name__)


async def convert_outline_prompt(
    outline: str, motor: MotorEnum = MotorEnum.MOTOR_A
) -> PROMPT_HANDLER_LIST:
    prompt_handler = await prompt_handler_factory(motor)

    with tracer.start_as_current_span("convert_outline_prompt") as span:
        outline_structured = {
            "1. SISTEMAS OPERACIONAIS": [
                "1.1. HISTÓRIA DOS SISTEMAS OPERACIONAIS",
                "1.2. GERENCIAMENTO DE PROCESSOS",
                "1.3. GERENCIAMENTO DE MEMÓRIA",
            ]
        }

        prompt_text = f"""
            Eu tenho o seguinte outline:

            {outline}

            E gostaria que você convertesse para essa estrutura, sem adicionar comentários a resposta:

            {outline_structured}
        """

        prompt = await prompt_handler(prompt_text)
        span.set_attribute("prompt", str(prompt.model_dump()))
        print(prompt)
        return prompt


async def course_detail_prompt(
    course: Course, 
    motor: MotorEnum = MotorEnum.MOTOR_A
) -> PROMPT_HANDLER_LIST:
    prompt_handler = await prompt_handler_factory(motor)

    with tracer.start_as_current_span("course_detail_prompt") as span:
        output_example = json.dumps(
            {
                "data": {
                    "generated_description": "description",
                    "generated_propose": "propose",
                    "generated_introduction": "introduction",
                    "generated_conclusion": "conclusion",
                }
            }
        )

        prompt_text = f"""
            You are an expert instructor specializing in creating educational 
            courses for '{course.name}'. You are tasked with developing a 
            comprehensive course presentation for prospective students. 
            The course is structured according to the following outline:

            {json.dumps(course.learning_topics)}

            In this outline, the first level represents the course modules, and 
            the second level details the specific topics covered within each module.

            Please generate the following content:

            * Course Description: Provide a concise course overview, summarizing 
            the main topics and objectives.

            * Course Purpose: Explain the importance of the course and what students 
            will gain from it.

            * Course Introduction: Offer a good introduction that catches the 
            interest of the course content giving the learners an idea of what 
            to expect, highlighting what students will explore throughout the modules.

            * Final Considerations: Create the Final Consideration including a 
            motivational closing that encourages students to apply the knowledge 
            they received from the course.

            Make sure to capture the essence and value of the course in each section, 
            making it appealing and informative for potential students.

            The result MUST be in Portuguese from Brazil and formatted to JSON 
            like the example below:

            {output_example}
        """

        prompt = await prompt_handler(prompt_text)
        span.set_attribute("prompt", str(prompt.model_dump()))
        print(prompt)
        return prompt


async def module_objective_prompt(
    course: Course,
    module_name: str,
    motor: MotorEnum = MotorEnum.MOTOR_A
) -> Union[PromptMotorA, PromptMotorB]:
    prompt_handler = await prompt_handler_factory(motor)

    with tracer.start_as_current_span("module_objectives_prompt") as span:

        prompt_text = f"""
        You are an expert instructor specializing in creating educational courses 
        for '{course.name}'. You only know write text in Brazilian Portuguese.
        
        Your task is to develop the specific goal for the  module '{module_name}'
        of the course, taking into consideration the topics outlined for the module.

        The course outline is:

        {json.dumps(course.learning_topics)}

        Write the objective without comments or additional information.

        Please ensure that each goal is clearly defined and accurately reflects 
        the content and objectives of the corresponding module.
        """

        prompt = await prompt_handler(prompt_text)
        span.set_attribute("prompt", str(prompt.model_dump()))
        print(prompt)
        return prompt


async def lesson_prompt(
    learning_topics: str,
    course_name: str,
    module_name: str,
    lesson_name: str,
    motor: MotorEnum = MotorEnum.MOTOR_A,
) -> Union[PromptMotorA, PromptMotorB]:
    prompt_handler = await prompt_handler_factory(motor)

    with tracer.start_as_current_span("lesson_prompt") as span:
        span.set_attribute("course_name", str(course_name))
        span.set_attribute("module_name", str(module_name))
        span.set_attribute("lesson_name", str(lesson_name))

        prompt_text = f"""
        You are an expert instructor specializing in creating educational courses 
        for '{course_name}'. You only know write text in Brazilian Portuguese.

        This course has the following outline:
        {learning_topics}

        In this outline, the first level represents the course modules, while the 
        second level specifies the topics covered within each module.

        Your task is to develop a comprehensive and detailed class for the topic 
        "{lesson_name}", ensuring rich and extended coverage.

        A thorough explanation of the concepts.
        Relevant examples to illustrate key points.

        The content should consist of at least 3000 words.

        Please ensure the content is comprehensive, engaging, and informative.

        Generate the text using Markdown format.
        """

        prompt = await prompt_handler(prompt_text)
        span.set_attribute("prompt", str(prompt.model_dump()))
        return prompt


async def lesson_video_script_prompt(
    lesson_content: str,
    motor: MotorEnum = MotorEnum.MOTOR_A,
) -> PROMPT_HANDLER_LIST:
    prompt_handler = await prompt_handler_factory(motor)

    prompt_text = f"""
    Act as a screenwriter expert in creating educational courses.
    The goal is to create a script for a short video with length 
    between 5 and 7 minutes.
    
    The video will be specific about the lesson rather than the 
    entire course.

    It should have the format of a testimonial video and, the video's 
    pedagogical objective is explanatory.

    Please remember that you only know how to write text in Brazilian 
    Portuguese and generate the text using Markdown format.

    Here is the lesson content:

    {lesson_content}
    """

    prompt = await prompt_handler(prompt_text)
    return prompt
