from django import template

from .. import utils

from ..models import ScavengerHuntSubmission


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


@register.filter
def distinct_scavenger_hunt_tasks(submissions):
    """Get distinct Scavenger Hunt tasks from a list of submissions"""
    return submissions.values('task').distinct()


@register.filter
def is_scavenger_hunt_task_submitted(task, group):
    return ScavengerHuntSubmission.objects.filter(task=task, group=group).exists()
