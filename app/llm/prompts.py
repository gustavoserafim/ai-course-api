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
        "data": {
            "module 1": "objective of module 1",
            "module 2": "objective of module 2",
        }
    })
    
    prompt = f"""
    Eu tenho o seguinte outline:

    {course.learning_topics}

    O primeiro nivel do outline é o nome do módulo e o segundo nível são os 
    assuntos que serão abordados nesse tópico.
        
    Gostaria que você gerasse para mim uma estrutura apenas com o nome do módulo 
    e escreva um objetivo para esse módulo baseado nos assuntos que serão abordados.

    No output você deve omitir as marcações númericas.

    Escreva a resposta em português do Brasil.

    Apresente a resposta no seguinte formato, sem adicionar comentários ao conteúdo:

    {output_example}
    """
    return prompt

async def content_prompt(
    course: Course,
    topic: str,
    subtopic: str
):
    with tracer.start_as_current_span("content_prompt") as span:
        span.set_attribute("Course", str(course.name))
        span.set_attribute("topic", str(topic))
        span.set_attribute("subtopic", str(subtopic))

        output_example = json.dumps({
            "content_blocks": [{
                "type": "TEXT",
                "content": "Texto sobre o tópico"
            }]
        })

        span.set_attribute("output_example", str(output_example))
        
        prompt = f"""
            Estou elaborando o conteúdo para um curso universitário 
            de "{course.name}" e gostaria que você gerasse para mim o conteúdo 
            academico completo da aula "{topic}" mais especificamente 
            sobre "{subtopic}", sem adicionar comentários ao conteúdo.

            Você deve gerar esse conteúdo em blocos.

            Especifique também o tipo de cada bloco: texto, imagem, 
            vídeo, lista de tópicos. Use os labels: IMAGE, TEXT, VIDEO.

            Importante que cada bloco tenha uma continuidade do bloco anterior.

            Quero que você escreva em Português do Brasil.

            O texto deve ter pelo menos 2000 palavras.

            Importante que o texto seja coeso e coerente e que tenha uma estrutura
            lógica com começo, meio e fim.

            Gostaria que o output fosse gerado em JSON. Seguindo o seguinte formato:

            {output_example}

            Não deve aparecer blocos incompletos que possam quebrar o JSON gerado.

            No caso de imagens ou videos, quero que o bloco tenha um prompt para a 
            geração desses conteúdos. Porem, é importante que você mantenha a estrutura
            sugerida.
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