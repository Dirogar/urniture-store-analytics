from django import template

register = template.Library()


@register.filter
def get_item(queryset, key):
    return queryset.get(key)

