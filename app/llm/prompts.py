import json
from app.models.course import Course

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def convert_outline_prompt(
        outline: str
) -> str:
    with tracer.start_as_current_span("convert_outline_prompt") as span:
        span.set_attribute("outline", str(outline))

        output_example = json.dumps({
            "outline": [{
                "topic": "Tópico 1",
                "subtopics": [
                    "Sub-tópico 1",
                    "Sub-tópico 2",
                    "Sub-tópico 3",
                    "Sub-tópico 4",
                ]
            }]
        })

        span.set_attribute("output_example", str(output_example))
        
        prompt = f"""
        Eu tenho o seguinte outline:

        {outline}

        O primeiro nivel do outline é o tópico e o segundo nivel é o sub-tópico.

        Gostaria que você convertesse esse outline para o seguinte formato, sem 
        adicionar comentários ao conteúdo:

        {output_example}
        """

        span.set_attribute("prompt", str(prompt))

        return prompt

async def module_objectives_prompt(course: Course) -> str:

    output_example = json.dumps({
        "data": [{
            "name": "module name",
            "objective": "generated objective of module",
            "subtopics": [
                "subtopic 1",
                "subtopic 2",
            ]
        }]
    })
    
    prompt = f"""
    Eu tenho o seguinte outline:

    {course.learning_topics}

    O primeiro nivel do outline é o nome do módulo e o segundo nível são os 
    nomes das aulas que serão abordados em cada tópico.
        
    Gostaria que você gerasse para mim uma estrutura, seguindo o seguinte 
    formato JSON, sem adicionar comentários ao conteúdo:
     
    {output_example}

    Observe que haverá apenas um objeto para o primeiro nível do outline.

    Os subtopicos estarão dentro da lista de subtópicos na estrutura sugerida.

    Escreva um objetivo para cada módulo baseado nos assuntos que serão abordados.

    No output você deve omitir as marcações númericas.

    Escreva a resposta em português do Brasil.
    """

    return prompt

async def lesson_prompt(
    course_name: str,
    module_name: str,
    lesson_name: str):

    with tracer.start_as_current_span("content_prompt") as span:
        span.set_attribute("course_name", str(course_name))
        span.set_attribute("module_name", str(module_name))
        span.set_attribute("lesson_name", str(lesson_name))
        
        prompt = f"""
            Estou elaborando o conteúdo para um curso universitário 
            de "{course_name}" e gostaria que você escreva para mim o conteúdo 
            academico completo da aula "{module_name}" mais especificamente 
            sobre "{lesson_name}", sem adicionar comentários ao conteúdo.

            Quero que você escreva em Português do Brasil.

            O texto deve ter pelo menos 3000 palavras.

            Quero que você escreva o conteúdo e não apenas uma estrutura de tópicos
            e subtópicos.

            Importante que o texto seja coeso e coerente e que tenha uma estrutura
            lógica com começo, meio e fim.

            
        """

        span.set_attribute("prompt", str(prompt))

        return prompt


async def course_detail_prompt(
        course: Course
) -> str:
    with tracer.start_as_current_span("course_detail_prompt") as span:
        span.set_attribute("Course", str(course.name))

        output_example = json.dumps({
            "data": {
                "generated_description": "description",
                "generated_propose": "propose",
                "generated_introduction": "introduction",
                "generated_conclusion": "conclusion",
            }
        })

        span.set_attribute("output_example", str(output_example))

        prompt = f"""
            Estou elaborando o conteúdo para um curso universitário de "{course.name}", 
            no qual eu desejo abordar os seguintes tópicos:

            {course.learning_topics}

            Gostaria que você gerasse para mim um conteúdo de apresentação do curso 
            para os alunos que vão cursa-lo com as seguintes informações, sem adicionar 
            comentários ao conteúdo:

            * Descrição do Curso
            * Propósito do Curso
            * Introdução do Curso
            * Considerações finais

            Gostaria que o output fosse gerado em JSON, seguindo o formato:

            {output_example}
        """

        span.set_attribute("prompt", str(prompt))

        return prompt