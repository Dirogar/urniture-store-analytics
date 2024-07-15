from django import template

register = template.Library()


@register.filter
def dict(value, arg):
    try:
        for key in value.items:
            value = value[key]
        a = value.get(value)
        return a
    except (KeyError, TypeError):
        return None
