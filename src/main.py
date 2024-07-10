import content
import helpers
import output

def generate_content(course_name: str, subject_name: str) -> dict:

    #
    # Generate course structure
    #

    course = content.generate_course(course=course_name, subject=subject_name)
    helpers.breakline()

    # only one chapter for testing propose
    chapter = course.get('chapters')[0]

    #
    # Generate outline for a chapter
    #
    outline = content.generate_outline(
       course=course_name,
       subject=subject_name,
       chapter=chapter
    )
    helpers.breakline()

    # get a topic and a subtopic for testing propose
    subtopic = outline.get('outline')[0].get('subtopics')[0]

    #
    # Generate the content for a subtopic
    #
    article = content.generate_content(
        course=course_name,
        subject=subject_name,
        topic=chapter,
        subtopic=subtopic,
    )
    helpers.breakline()

    """
    We need to interate over the chapters and over the 
    subtopics to generate the content for each subtopic
    and create an output list with all the content
    """

    return article



if __name__ == "__main__":
    content = generate_content(
       course_name="Ciências da Computação",
       subject_name="Introdução aos Sistemas Operacionais")

    html = output.to_html(content)

    with open('output.html', 'w', encoding='utf-8') as f:
      f.write(html)