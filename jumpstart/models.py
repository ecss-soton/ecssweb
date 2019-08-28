from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator
import os
import uuid
from .validators import validate_photo_file_extension

from auditlog.models import AuditLog


def helper_photo_file_name(instance, filename):
    return ('jumpstart2018/helpers/{}-{}{}'.format(instance.username, uuid.uuid4(), os.path.splitext(filename)[1].lower()))


def charity_shop_challenge_photo_file_name(instance, filename):
    return ('jumpstart2018/city-challenge/charity-shop-challenge-group{}-{}{}'.format(instance.id, uuid.uuid4(), os.path.splitext(filename)[1].lower()))


def scavenger_hunt_photo_file_name(instance, filename):
    return ('jumpstart2018/city-challenge/scavenger-hunt-group{}-{}{}'.format(instance.group.id, uuid.uuid4(), os.path.splitext(filename)[1].lower()))


class Group(models.Model):
    number = models.PositiveSmallIntegerField(unique=True, validators=[MinValueValidator(1)], verbose_name='Group Number')
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Group Name')
    charity_shop_challenge_photo = models.ImageField(upload_to=charity_shop_challenge_photo_file_name, validators=[validate_photo_file_extension], null=True, blank=True, verbose_name='Charity Shop Challenge Photo')
    mitre_challenge_score = models.IntegerField(null=True, blank=True)
    coding_challenge_score = models.IntegerField(null=True, blank=True)
    stags_quiz_score = models.IntegerField(null=True, blank=True)
    games_challenge_score = models.IntegerField(null=True, blank=True)
    sports_challenge_score = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return 'Group {}'.format(self.number)


class Fresher(models.Model):
    username = models.CharField(max_length=20, primary_key=True, verbose_name='Username')
    name = models.CharField(max_length=50, verbose_name='Name')
    prefered_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Prefered Name')
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='Group')
    is_checked_in = models.BooleanField(default=False, null=False, verbose_name='Checked In')


    def __str__(self):
        return self.username


class Helper(models.Model):
    username = models.CharField(max_length=20, primary_key=True, verbose_name='Username')
    name = models.CharField(max_length=50, verbose_name='Name')
    prefered_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Preferend Name')
    photo = models.ImageField(upload_to=helper_photo_file_name, blank=True, validators=[validate_photo_file_extension], verbose_name='Photo')
    group = models.OneToOneField(Group, on_delete=models.PROTECT, verbose_name='Group')


    def __str__(self):
        return self.username


class ScavengerHunt(models.Model):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to=scavenger_hunt_photo_file_name, validators=[validate_photo_file_extension])


class CityChallengeScoreAuditlog(models.Model):
    user = models.CharField(max_length=150)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    challenge = models.CharField(max_length=150)
    score = models.IntegerField()

    auditlog = GenericRelation(AuditLog)

    def __str__(self):
        return '{} updated score of for {} for Group {} to {} at {}'.format(self.user, self.challenge, self.group.id, self.score, self.auditlog.get().time)
