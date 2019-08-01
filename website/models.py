from django.db import models
from django.template.defaultfilters import slugify

import os


# Committee

def committee_member_image_file_name(instance, filename):
    return ('committee/{}-{}{}'.format(instance.role_codename, slugify(instance.member_name), os.path.splitext(filename)[1].lower()))

# Simple model works for each role held by only one member.
# In cases of change of circumstances, this model might need to be rewritten though it might be possible to continue using this model with some workaround.
class CommitteeRoleMember(models.Model):
    role_codename = models.CharField(max_length=50, primary_key=True)
    role_short_name = models.CharField(max_length=50, default='')
    role_name = models.CharField(max_length=100)
    role_description = models.TextField()
    member_name = models.CharField(max_length=100)
    member_nickname = models.CharField(max_length=50, blank=True)
    member_image = models.ImageField(upload_to=committee_member_image_file_name)
    member_manifesto = models.TextField()
    member_email = models.EmailField(max_length=100)
    member_facebook = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = 'committee roles members'

    def __str__(self):
        return '{} ({})'.format(self.role_name, self.member_name)


# Societies


def society_logo_image_file_name(instance, filename):
    return ('societies/{}{}'.format(instance.codename, os.path.splitext(filename)[1].lower()))


class Society(models.Model):
    codename = models.CharField(max_length=50, primary_key=True)
    short_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=society_logo_image_file_name)

    description = models.TextField(blank=True)

    time = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    fb_page = models.URLField(blank=True)
    fb_group = models.URLField(blank=True)
    twitter = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'societies'

    def __str__(self):
        return self.name


class SocietyLink(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.URLField()

    class Meta:
        verbose_name_plural = 'societies links'

    def __str__(self):
        return '{} - {}'.format(self.society, self.name)


# Sponsors

class Sponsor(models.Model):
    codename = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    level = models.CharField(choices=[('gold', 'gold'), ('silver', 'silver'), ('bronze', 'bronze')], max_length=20)
    logo_file = models.CharField(max_length=100)

    description = models.TextField()
    website = models.URLField()

    def __str__(self):
        return self.name


class SponsorLink(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.URLField()

    class Meta:
        verbose_name_plural = 'sponsors links'

    def __str__(self):
        return '{} - {}'.format(self.sponsor, self.name)
