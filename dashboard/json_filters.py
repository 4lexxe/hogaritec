# dashboard/templatetags/json_filters.py
import json
from django import template

register = template.Library()

@register.filter
def jsonify(value):
    """Convierte un objeto Python a JSON."""
    return json.dumps(value)
