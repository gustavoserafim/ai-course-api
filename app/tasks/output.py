import os
from collections import defaultdict
from typing import List, Dict, Any

from jinja2 import Environment, FileSystemLoader
from opentelemetry import trace
from slugify import slugify


tracer = trace.get_tracer(__name__)

template_dir = os.path.join(os.path.dirname(__file__), '../templates')

def regroup(data: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    grouped_data = defaultdict(list)
    for item in data:
        grouped_data[item[key]].append(item)
    return [{"grouper": k, "list": v} for k, v in grouped_data.items()]

def filter_by(data, key, value):
    return [item for item in data if item.get(key) == value]


env = Environment(loader=FileSystemLoader(template_dir))
env.filters['slugify'] = slugify
env.filters['filter_by'] = filter_by

template = env.get_template('course.html')

def to_html(context):
  with tracer.start_as_current_span("to_html") as span:
      span.set_attribute("context", str(context))
      output = template.render(context)
      # with open('course.html', 'w') as f:
      #     f.write(output)
      return output
      
