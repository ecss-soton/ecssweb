from django.db import models

from django.contrib.auth.models import User, Group

class SamlUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_persistent = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ("is_ecs_user", "The user is within ECS"),
        )

class EcsswebUserGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    is_saml = models.BooleanField(default=False)

class ConsumedAssertionRecord(models.Model):
    assertion_id = models.CharField(max_length=100, primary_key=True)
    not_on_or_after = models.DateTimeField(db_index=True)
