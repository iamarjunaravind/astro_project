
from django import template

register = template.Library()

@register.filter
def are_equal(val1, val2):
    """
    Compares two values for equality.
    Usage: {% if value1|are_equal:value2 %}
    Useful to avoid TemplateSyntaxErrors caused by aggressive auto-formatters stripping logic operators.
    """
    return str(val1) == str(val2)
