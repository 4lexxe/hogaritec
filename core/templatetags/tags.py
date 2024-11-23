# core/templatetags/tags.py

from django import template

register = template.Library()

@register.simple_tag
def my_tag(arg):
    return f"Este es un tag que recibe: {arg}"
