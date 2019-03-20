from django import template
import random


register = template.Library()


@register.filter
def msort(l, key):
    return l.order_by(key)


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def shuffle(l):
    l = list(l)
    random.shuffle(l)
    return l
