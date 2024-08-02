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
    course: Course, motor: MotorEnum = MotorEnum.MOTOR_A
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

        # prompt
        prompt_text = f"""
            Você é especialista em desenvolvimento de conteúdo instrucional de um 
            curso universitário de '{course.name}' e está elaborando uma apresentação
            do curso para para os alunos que irão cursa-lo.

            O curso que você está elaborando possui o seguinte ouline:

            {course.outline_structured}

            Onde, o primeiro nível do outline é o nome do módulo do curso e
            o segundo nível do outline são os assuntos que serão abordados em
            cada módulo.

            Quero que você gere o conteúdo abaixo:

            1. **Descrição do Curso**: Resumo dos principais temas e objetivos.
            2. **Propósito do Curso**: Importância e o que os alunos irão aprender.
            3. **Introdução do Curso**: Resumo do que os alunos explorarão.
            4. **Considerações Finais**: Incentivo para matricular-se e benefícios.

            Formato JSON desejado, não adicione comentários na resposta:

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
            Eu tenho o seguinte outline:

            {json.dumps(course.outline_structured)}

            Essa estrutura possui tópicos e subtópicos. Os tópicos representam
            o nome dos módulos e os sub-tópicos representam os assuntos que serão
            abordados no módulo.

            Gostaria que você escrevesse um objetivo para cada módulo.
            
            O resultado deve seguir o formato JSON válido, sem adicionar 
            comentários ao conteúdo:
            
            {output_example}

            Certifique-se de que não haja vírgulas extras após o último item em 
            qualquer array ou objeto.

            Observe que haverá apenas um objeto para o primeiro nível do outline.

            Os subtopicos estarão dentro da lista de subtópicos na estrutura sugerida.

            Escreva um objetivo para cada módulo baseado nos assuntos que serão abordados.

            No output você deve omitir as marcações númericas.

            Escreva a resposta em português do Brasil.
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
