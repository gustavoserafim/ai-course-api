import json
from typing import List

from pydantic import BaseModel
from app.models.course import Course

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class PromptMessage(BaseModel):
    role: str
    content: str

class Prompt(BaseModel):
    max_new_tokens: int = 2000
    temperature: float = 0.1
    top_p: float = 0.95
    repetition_penalty: float = 1.2
    messages: List[PromptMessage]

async def convert_outline_prompt(outline: str) -> Prompt:

    with tracer.start_as_current_span("convert_outline_prompt") as span:

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
        
        prompt_text = f"""
        Imagine que você está organizando um curso universitário.
        O seguinte esboço do conteúdo foi fornecido:

        {outline}

        O primeiro nível do esboço representa os tópicos principais do curso,
        enquanto o segundo nível detalha os subtópicos a serem abordados em cada tópico.
        Sua tarefa é estruturar esse esboço de forma mais organizada,
        utilizando o formato JSON demonstrado abaixo.
        Lembre-se de manter a formatação JSON consistente.

        {output_example}
        """
        prompt_message = PromptMessage(
            role="user",
            content=prompt_text)

        prompt = Prompt(messages=[prompt_message])

        span.set_attribute("prompt", str(prompt.model_dump()))

        return prompt

async def module_objectives_prompt(course: Course) -> Prompt:

    with tracer.start_as_current_span("module_objectives_prompt") as span:

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
        
        prompt_text = f"""
        Você é um especialista em design instrucional, auxiliando na elaboração de 
        um curso universitário chamado "{course.name}".

        Seu objetivo é formular objetivos de aprendizagem claros, concisos e 
        mensuráveis para cada módulo do curso, com base no seguinte esboço de conteúdo:

        {course.learning_topics}

        Neste esboço:
        * O primeiro nível representa o nome de cada módulo.
        * O segundo nível lista as aulas específicas que compõem cada módulo.

        Ao formular os objetivos, siga estas diretrizes:
        * **Orientação para o aluno:**  Concentre-se no que os alunos serão capazes de fazer após concluir o módulo.
        * **Clareza e Especificidade:** Use verbos de ação mensuráveis (ex: analisar, aplicar, avaliar, criar).
        * **Alinhamento com o Conteúdo:**  Garanta que os objetivos reflitam os tópicos e subtópicos listados.

        Estruture sua resposta no formato JSON demonstrado abaixo, incluindo os 
        subtópicos exatamente como aparecem no esboço original:

        {output_example}

        Lembre-se:
        * Mantenha a formatação JSON consistente.
        * Omita as marcações numéricas no output.
        * Escreva em português do Brasil.
        """

        prompt_message = PromptMessage(
            role="user",
            content=prompt_text)
        
        prompt = Prompt(messages=[prompt_message])

        span.set_attribute("prompt", str(prompt.model_dump()))

    return prompt

async def lesson_prompt(course_name: str, module_name: str, lesson_name: str) -> Prompt:

    with tracer.start_as_current_span("lesson_prompt") as span:
        span.set_attribute("course_name", str(course_name))
        span.set_attribute("module_name", str(module_name))
        span.set_attribute("lesson_name", str(lesson_name))
        
        prompt_text = f"""
            Você está auxiliando na criação de um curso universitário 
            chamado "{course_name}". Sua tarefa é elaborar o conteúdo da 
            aula "{lesson_name}", que faz parte do módulo "{module_name}".

            Ao elaborar o conteúdo, siga estas diretrizes:
            * **Público-alvo:** Estudantes universitários.
            * **Extensão:**  Aproximadamente 3000 palavras.
            * **Estrutura:** Apresentação, desenvolvimento de conceitos-chave, exemplos, estudos de caso (se aplicável), conclusão.
            * **Linguagem:** Português do Brasil, formal, clara, concisa e adequada ao público.
            * **Engajamento:** Inclua exemplos, perguntas reflexivas e conexões com o mundo real para tornar o aprendizado mais eficaz.

            Lembre-se:
            *  Seu objetivo é criar uma experiência de aprendizado completa e envolvente.
            *  Não adicione comentários ao conteúdo.
        """

        prompt_message = PromptMessage(
            role="user",
            content=prompt_text)
        prompt = Prompt(messages=[prompt_message])
        span.set_attribute("prompt", str(prompt.model_dump()))
        return prompt

async def course_detail_prompt(course: Course) -> Prompt:

    with tracer.start_as_current_span("course_detail_prompt") as span:

        output_example = json.dumps({
            "data": {
                "generated_description": "description",
                "generated_propose": "propose",
                "generated_introduction": "introduction",
                "generated_conclusion": "conclusion",
            }
        })

        prompt_text = f"""
            Imagine que você está criando um conteúdo educacional rico e 
            envolvente para um curso universitário chamado "{course.name}". 
            
            Seu objetivo é apresentar o curso de forma clara, concisa e 
            inspiradora para potenciais alunos. Utilize os seguintes tópicos 
            como base para o conteúdo: 
            
            {course.learning_topics}.
            
            Estruture o conteúdo em seções distintas conforme o exemplo abaixo, 
            incluindo exemplos de cada seção: 
            
            ### Exemplo de Estrutura de Conteúdo:

            1. **Descrição do Curso**: Uma visão geral do curso, destacando seus 
            principais temas e objetivos.
            
            - Exemplo: "Este curso explora os fundamentos da inteligência 
            artificial, abordando temas como aprendizado de máquina, redes 
            neurais e processamento de linguagem natural. Os alunos desenvolverão 
            habilidades práticas e teóricas para aplicar IA em diversas áreas."
            
            2. **Propósito do Curso**: Por que este curso é importante? O que os 
            alunos aprenderão e como isso os beneficiará? 
            
            - Exemplo: "O propósito deste curso é capacitar os alunos a compreender 
            e aplicar técnicas de IA para resolver problemas complexos. Ao concluir 
            o curso, os alunos estarão preparados para carreiras em ciência de dados, 
            desenvolvimento de software e pesquisa."
            
            3. **Introdução do Curso**: Um resumo conciso do que os alunos explorarão 
            ao longo do curso. 
            
            - Exemplo: "Neste curso, você explorará os conceitos  fundamentais da IA, 
            desde algoritmos básicos até técnicas avançadas. Aprenderá a desenvolver 
            modelos preditivos, analisar dados e implementar soluções de IA."
            
            4. **Considerações Finais**: Incentive os alunos a se matricularem, 
            destacando os benefícios de participar do curso. 
            
            - Exemplo: "Ao se matricular neste curso, você terá acesso a recursos 
            exclusivos, mentoria de especialistas e oportunidades de networking 
            com profissionais da indústria. Inscreva-se agora e inicie sua jornada na IA!"

            Formato JSON desejado:

            {output_example}
        """

        prompt_message = PromptMessage(
            role="user",
            content=prompt_text)
        
        prompt = Prompt(messages=[prompt_message])

        span.set_attribute("prompt", str(prompt.model_dump()))

        return prompt