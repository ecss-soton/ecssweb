from django.db import models


# Societies

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


class SocietyLink(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.URLField()


# Sponsors

class Sponsor(models.Model):
    codename = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    level = models.CharField(choices=[('gold', 'gold'), ('silver', 'silver'), ('bronze', 'bronze')], max_length=20)
    logo_file = models.CharField(max_length=100)

    description = models.TextField()
    website = models.URLField()

class SponsorLink(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.URLField()
