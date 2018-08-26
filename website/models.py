from django.db import models


class Society(models.Model):
    codename = models.CharField(max_length=50, primary_key=True)
    short_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    logo_file = models.CharField(max_length=100)

    description = models.TextField()

    time = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.URLField()

    fb_page = models.URLField()
    fb_group = models.URLField()
    twitter = models.CharField(max_length=100)


class SocietyLinks(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.URLField()
