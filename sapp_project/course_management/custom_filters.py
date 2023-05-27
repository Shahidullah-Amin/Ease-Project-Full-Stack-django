import os
from django import template



register = template.Library()

@register.filter
def basename(file_path):
    return os.path.basename(file_path)


