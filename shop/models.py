from django.db import models


class sale(models.Model):
    codename = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    start = models.DateTimeField()
    


class item(models.Model):
    codename = models
    name = models.CharField(max_length=50, primary_key=True)
    image = models.ImageField()
