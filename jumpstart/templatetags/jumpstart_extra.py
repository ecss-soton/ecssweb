from django import template

from .. import utils


register = template.Library()


@register.filter
def is_fresher(user):
    return utils.is_fresher(user)


@register.filter
def is_helper(user):
    return utils.is_helper(user)


@register.filter
def checked_in_freshers(freshers):
    """Get checked in Freshers from a list."""
    return [fresher for fresher in freshers if fresher.is_checked_in]
