from website.utils import is_committee

from .models import Fresher, Helper


def is_fresher(user):
    return Fresher.objects.filter(pk=user.username).exists()

def is_helper(user):
    return Helper.objects.filter(pk=user.username).exists()

def jumpstart_check(user):
    return is_committee or is_fresher or is_helper
