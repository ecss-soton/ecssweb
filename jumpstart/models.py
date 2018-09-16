from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Fresher(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
