from django import template

register = template.Library()

@register.filter(name='split_get_end')
def split_get_end(value, args):
    return value.split(args)[-1]