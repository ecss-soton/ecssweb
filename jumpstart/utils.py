from .models import Fresher


def jumpstart_check(user):
    return user.groups.filter(name='committee').exists() \
        or Fresher.objects.filter(pk=user.username).exists()
