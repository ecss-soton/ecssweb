from django.db import models

from django.contrib.auth.models import User, Group

class SamlUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_persistent = models.BooleanField(default=False)

class EcsswebUserGroup(models.Model):
    user = models.OneToOneField(Group, on_delete=models.CASCADE)
    is_saml = models.BooleanField()
