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
                    "generated_description:": "description",
                    "generated_propose:": "propose",
                    "generated_introduction:": "introduction",
                    "generated_conclusion:": "conclusion",
                }
            }
        )

        prompt_text = f"""
            You are an expert instructor specializing in creating educational 
            courses for '{course.name}'. You are tasked with developing a 
            comprehensive course presentation for prospective students. 
            The course is structured according to the following outline:

            {json.dumps(course.outline_structured)}

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


async def module_objectives_prompt(
    course: Course, motor: MotorEnum = MotorEnum.MOTOR_A
) -> Union[PromptMotorA, PromptMotorB]:
    prompt_handler = await prompt_handler_factory(motor)

    with tracer.start_as_current_span("module_objectives_prompt") as span:
        output_example = json.dumps(
            {
                "data": [
                    {
                        "name": "module name",
                        "objective": "generated objective of module",
                        "subtopics": ["subtopic 1", "subtopic 2"],
                    }
                ]
            }
        )

        prompt_text = f"""
        You are an expert instructor specializing in creating educational courses 
        for '{course.name}'. Your task is to develop the specific goals for each 
        module of the course, taking into consideration the topics outlined for 
        each module.

        The course outline is:

        {json.dumps(course.outline_structured)}

        The result MUST be in Portuguese from Brazil and formatted as JSON, 
        following the example provided below:
            
        {output_example}

        Please ensure that each goal is clearly defined and accurately reflects 
        the content and objectives of the corresponding module. The objective must 
        be in Portuguese and the subtopics without the numbers.
        """

        prompt = await prompt_handler(prompt_text)
        span.set_attribute("prompt", str(prompt.model_dump()))
        print(prompt)
        return prompt


async def lesson_prompt(
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
            Você está desenvolvendo o conteúdo para o curso universitário 
            "{course_name}", especificamente para a aula "{lesson_name}", que 
            pertence ao módulo "{module_name}".
            
            Siga as diretrizes abaixo:
            
            * **Público-alvo:** Estudantes universitários. 
            * **Extensão:** Aproximadamente 3000 palavras. 
            * **Estrutura:** Apresentação, desenvolvimento de conceitos-chave, 
              exemplos, estudos de caso (se houver), conclusão. 
            * **Linguagem:** Português do Brasil, formal, clara e concisa. 
            * **Engajamento:** Inclua exemplos, perguntas reflexivas e conexões 
              com o mundo real para facilitar o aprendizado. Mantenha o foco em 
              criar uma experiência de aprendizado completa e envolvente, sem 
              adicionar comentários ao conteúdo.
        """
        prompt = await prompt_handler(prompt_text)
        span.set_attribute("prompt", str(prompt.model_dump()))
        return prompt
