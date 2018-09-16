from .models import Fresher, Helper


def jumpstart_check(user):
    return user.groups.filter(name='committee').exists() \
        or Fresher.objects.filter(pk=user.username).exists() \
        or Helper.objects.filter(pk=user.username).exists()
