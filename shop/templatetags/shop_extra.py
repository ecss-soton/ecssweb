from django import template
from django.contrib.auth.models import Permission


from ..utils import has_any_perms_item as _has_any_perms_item


register = template.Library()


@register.filter
def has_any_perms_item(user, item):
    return _has_any_perms_item(user, item)
