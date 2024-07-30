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
    return float(queryset * 2)


@register.filter(name='dictkey')
def dictkey(value, arg):
    try:
        if value:
            return value[arg]
        else:
            return 0
    except KeyError:
        return 0


@register.filter(name='status_color')
def status_color(status):
    if status == 'Выполнено':
        return 'text-success'
    elif status == 'В работе':
        return 'text-warning'
    else:
        return 'text-danger'
