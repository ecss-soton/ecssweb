from django.db import models

from django.contrib.auth.models import User, Group


class SamlUserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, user_name):
        return self.get(user=User.objects.db_manager(self.db).get_by_natural_key(user_name))

class SamlUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_persistent = models.BooleanField(default=False)

    objects = SamlUserManager()

    def natural_key(self):
        return (self.user.username,)

    def __str__(self):
        return str(self.user)

    class Meta:
        permissions = (
            ("is_ecs_user", "The user is within ECS"),
        )


class EcsswebUserGroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, group_name):
        return self.get(group=Group.objects.db_manager(self.db).get_by_natural_key(group_name))

class EcsswebUserGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    is_saml = models.BooleanField(default=False)

    objects = EcsswebUserGroupManager()

    def natural_key(self):
        return (self.group.name,)

    def __str__(self):
        return str(self.group)


class ConsumedAssertionRecord(models.Model):
    assertion_id = models.CharField(max_length=100, primary_key=True)
    not_on_or_after = models.DateTimeField(db_index=True)
