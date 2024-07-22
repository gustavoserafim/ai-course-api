from jinja2 import Environment, FileSystemLoader
import os
from slugify import slugify

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))
env.filters['slugify'] = slugify

template = env.get_template('course.html')

def to_html(
      context
):
  with tracer.start_as_current_span("to_html") as span:
      span.set_attribute("context", str(context))
      return template.render(context)
