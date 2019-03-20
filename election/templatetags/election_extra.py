from django import template
from ..models import Support, Voter
from django.db.models import Q


register = template.Library()


@register.filter
def is_supporting(nomination, user):
    return Support.objects.filter(Q(nomination=nomination) & Q(supporter=user.username))


@register.filter
def has_voted(position, user):
    return Voter.objects.filter(username=user.username, position=position).exists()
