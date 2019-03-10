from django import template
from ..models import Support
from django.db.models import Q


register = template.Library()


@register.filter
def is_supporting(nomination, user):
    return Support.objects.filter(Q(nomination=nomination) & Q(supporter=user.username))
