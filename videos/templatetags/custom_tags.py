from django import template
register = template.Library()

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)

@register.filter(name='times')
def times(number):
    return range(int(1.0), int(number) + int(1.0))