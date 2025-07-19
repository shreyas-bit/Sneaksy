# shop/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by the arg."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return ''
