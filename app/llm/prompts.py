import json
from typing import Awaitable, Union

from opentelemetry import trace

from app.models.course import Course
from app.llm.models import PROMPT_HANDLER_LIST, MotorEnum, PromptMotorA, PromptMotorB, prompt_handler_factory

tracer = trace.get_tracer(__name__)


async def course_detail_prompt(
    course: Course,
    motor: MotorEnum = MotorEnum.MOTOR_A) -> PROMPT_HANDLER_LIST:

    prompt_handler = await prompt_handler_factory(motor)

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
        prompt = await prompt_handler(prompt_text)
        span.set_attribute("prompt", str(prompt.model_dump()))
        return prompt

async def module_objectives_prompt(
    course: Course, 
    motor: MotorEnum = MotorEnum.MOTOR_A) -> Union[PromptMotorA, PromptMotorB]:

    prompt_handler = await prompt_handler_factory(motor)

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
            Conteúdo:
            {course.learning_topics}

            Você é um especialista em design instrucional auxiliando na elaboração de 
            um curso universitário chamado '{course.name}'. Sua tarefa é gerar um 
            objetivo de aprendizagem claro e mensurável para o 
            cada módulo do conteúdo fornecido.
            
            O objetivo deve ser definido com foco no que os alunos serão capazes de 
            fazer após completar o módulo e deve estar alinhado com os tópicos listados. 
            Certifique-se de utilizar verbos de ação mensuráveis (por exemplo, analisar, 
            aplicar, avaliar, criar). O resultado deve ser estruturado em JSON conforme 
            o seguinte exemplo:

            {output_example}
        """
        prompt = await prompt_handler(prompt_text)
        span.set_attribute("prompt", str(prompt.model_dump()))
        return prompt

async def lesson_prompt(
    course_name: str,
    module_name: str,
    lesson_name: str,
    motor: MotorEnum = MotorEnum.MOTOR_A
) -> Union[PromptMotorA, PromptMotorB]:
    
    prompt_handler = await prompt_handler_factory(motor)

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
        prompt = await prompt_handler(prompt_text)
        span.set_attribute("prompt", str(prompt.model_dump()))
        return prompt