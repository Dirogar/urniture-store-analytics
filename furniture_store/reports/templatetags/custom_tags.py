from django import template

register = template.Library()


@register.filter
def get_item(queryset, key):
    return queryset.get(key)


@register.filter
def default_if_none(queryset, key):
    return queryset or 0


@register.filter()
def square(queryset: float):
    return float(queryset*2)

