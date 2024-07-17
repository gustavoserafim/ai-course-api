import json
from app.models.course import Course

async def convert_outline_prompt(outline: str) -> str:
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
    
    prompt = f"""
    Eu tenho o seguinte outline:

    {outline}

    O primeiro nivel do outline é o tópico e o segundo nivel é o sub-tópico.

    Gostaria que você convertesse esse outline para o seguinte formato, sem 
    adicionar comentários ao conteúdo:

    {output_example}
    """
    return prompt

async def content_prompt(
    course: Course,
    topic: str,
    subtopic: str):

    output_example = json.dumps({
        "content_blocks": [{
            "type": "TEXT",
            "content": "Texto sobre o tópico"
        }]
    })
      
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

    return prompt
