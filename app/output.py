from jinja2 import Environment, FileSystemLoader
import os
from slugify import slugify

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))
env.filters['slugify'] = slugify

template = env.get_template('course.html')

def to_html(context):
  return template.render(context)
