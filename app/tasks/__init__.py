import json
import time
import traceback
from app.models.course import Course
from app.services.content_service import ContentService
from app.llm.generator import generate_outline, generate_content
from app.api.endpoints.websocket import manager as ws

async def task_generate_content(
    course: Course,
    content_service: ContentService) -> None:

    start_time = time.time() 

    try:
        # create outline
        outline = await generate_outline(course.learning_topics)
        print(outline)

        for section in outline.get('outline', []):
            topic = section.get('topic')
            subtopic_list = section.get('subtopics', [])
            for subtopic in subtopic_list:
                print(f"Generating content for {topic} - {subtopic}")
                subtopic_content = await generate_content(
                    course=course,
                    topic=topic,
                    subtopic=subtopic)
                # save_content(subtopic)
        
        print("TASK COMPLETED")
        await ws.broadcast(json.dumps({
            "message": f'Content for "{course.name}" generation completed',
            "status": "COMPLETED"
        }))


    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f}.")

    # content = ContentCreate(
    #     course_id=str(course.id),
    #     name="Generated Content",
    #     content=[
    #         ContentBlock(
    #             type="text", 
    #             content="This is a generated content block")
    #     ])

    # await content_service.create_content(content)
