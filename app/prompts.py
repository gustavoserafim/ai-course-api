import json

def course_prompt(course: str, subject: str) -> str:
    output_example = json.dumps({
        "course": "Course Name",
        "subject": "Subject of course",
        "chapters": [
            "Chapter 1",
            "Chapter 2",
        ]
    })
    
    prompt = f"""
    Estou montando um módulo para um curso universitário de "{course}", para 
    matéria de "{subject}" e gostaria que você gerasse para mim uma lista de
    capitulos que eu devo abordar no curso, sem adicionar comentários ao conteúdo.

    Gostaria que você gerasse pelo menos 15 assuntos, em Português do Brasil.

    Gostaria que o output fosse gerado em JSON. Seguindo o seguinte formato:

    {output_example}

    Tome o cuidado para gerar apenas uma vez essa estrutura.

    É importante que você gere apenas a estrutura no formato que eu estou
    pedindo. Não há necessidade de explicar o conteúdo gerado.
    """
    return prompt

def outline_prompt(course: str, subject: str, chapter: str) -> str:
    output_example = json.dumps({
        "course": "Course Name",
        "subject": "Subject of course",
        "outline": [
            {
                "topic": "Tópico 1",
                "subtopics": [
                    "Sub-tópico 1",
                    "Sub-tópico 2",
                    "Sub-tópico 3",
                    "Sub-tópico 4",
                ]
            }
        ]
    })
    
    prompt = f"""
    Estou montando um módulo para um curso universitário de "{course}", para 
    matéria de "{subject}" mais especificamente sobre o capitulo de "{chapter}"
    e gostaria que você gerasse para mim um outline em Português do Brasil sobre 
    o que seria interessante abordar, sem adicionar comentários ao conteúdo.

    Gostaria que você gerasse pelo menos 10 tópicos, e cada tópico deve ter
    pelo menos 4 sub-tópicos.

    Gostaria que o output fosse gerado em JSON. Seguindo o seguinte formato:

    {output_example}
    """
    return prompt

def content_prompt(
    course: str,
    subject: str,
    topic: str,
    subtopic: str,
    image_quantity: int = 2, 
    has_video: bool = False):

    output_example = json.dumps({
      "content_blocks": [{
          "type": "TEXT",
          "content": "Texto sobre o tópico"
      }]
    })

    prompt_image = image_quantity \
        and f"Cada aula deve ter pelo menos {image_quantity} blocos imagens" \
        or ""
      
    prompt_video = has_video \
        and "Cada aula deve ter pelo menos um bloco de vídeo" \
        or ""
      
    prompt = f"""
        Crie um conteúdo educacional sobre o curso para um curso universitário 
        de "{course}", para matéria "{subject}" e gostaria que você gerasse para 
        mim o conteúdo completo da aula "{topic}" mais especificamente sobre "{subtopic}",
        sem adicionar comentários ao conteúdo.

        Você deve gerar esse conteúdo em blocos.

        Especifique também o tipo de cada bloco: texto, imagem, 
        vídeo, lista de tópicos. Use os labels: IMAGE, TEXT, VIDEO, LIST.

        Importante que cada bloco tenha uma continuidade do bloco anterior.

        {prompt_image}

        {prompt_video}

        No caso de imagens ou videos, quero que o bloco tenha um prompt para a 
        geração desses conteúdos.

        Quero que você escreva em Português do Brasil.

        O texto deve ter pelo menos 2000 palavras.

        Gostaria que o output fosse gerado em JSON. Seguindo o seguinte formato:

        {output_example}
    """

    return prompt
