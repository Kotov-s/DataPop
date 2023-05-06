from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def include_html(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return mark_safe(content)
