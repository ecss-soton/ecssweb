from django.db import models
import os
import uuid
from .validators import validate_photo_file_extension


def photo_file_name(instance, filename):
    return ('jumpstart2018/helpers/{}-{}{}'.format(instance.username, uuid.uuid4(), os.path.splitext(filename)[1].lower()))

class Group(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Fresher(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

class Helper(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to=photo_file_name, validators=[validate_photo_file_extension])
    group = models.OneToOneField(Group, on_delete=models.SET_NULL, null=True)
