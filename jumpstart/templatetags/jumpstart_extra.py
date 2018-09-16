from django import template

from ..models import Fresher, Helper

from .. import utils

register = template.Library()

@register.filter
def is_fresher(user):
    return utils.is_fresher(user)

@register.filter
def is_helper(user):
    return utils.is_helper(user)
