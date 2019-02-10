from django.contrib.auth.models import Permission

from .models import ItemPermission


def has_any_perms_item(user, item):
    item_perms = ItemPermission.objects.filter(item=item)
    if not item_perms.exists():
        return True
    perms = set(item_perm.permission for item_perm in item_perms)
    user_perms = set(perm for perm in user.user_permissions.all() | Permission.objects.filter(group__user=user))
    return user_perms & perms
