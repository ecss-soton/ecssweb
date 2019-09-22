from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import os
import uuid
from django.utils import timezone
from .validators import validate_photo_file_extension

from auditlog.models import AuditLog


def helper_photo_file_name(instance, filename):
    return ('jumpstart/helpers/group-{}-{}-{}{}'.format(instance.group.number, slugify(instance.name), uuid.uuid4(), os.path.splitext(filename)[1].lower()))


def charity_shop_challenge_photo_file_name(instance, filename):
    return ('jumpstart/city-challenge/charity-shop-challenge-group{}-{}{}'.format(instance.id, uuid.uuid4(), os.path.splitext(filename)[1].lower()))


def scavenger_hunt_photo_file_name(instance, filename):
    return ('jumpstart2018/city-challenge/scavenger-hunt-group{}-{}{}'.format(instance.group.id, uuid.uuid4(), os.path.splitext(filename)[1].lower()))


'''
Jumpstart config, does not link to other models (except Site so only one is allowed).
'''
class Jumpstart(models.Model):
    site = models.OneToOneField(Site, on_delete=models.PROTECT)
    start_time = models.DateTimeField(verbose_name='Start Time')
    end_time = models.DateTimeField(verbose_name='End Time')
    helper_profile_lock_time = models.DateTimeField(verbose_name='Helper Profile Lock Time')


    def clean(self):
        super(Jumpstart, self)
        if self.start_time > self.end_time:
            raise ValidationError('End time cannot be earlier than start time.')
        if self.helper_profile_lock_time > self.start_time:
            raise ValidationError('Helper profile lock time cannot be later than start time.')


    @property
    def is_before(self):
        return timezone.now() < self.start_time


    @property
    def is_now(self):
        return timezone.now() >= self.start_time and timezone.now() <= self.end_time


    @property
    def is_after(self):
        return timezone.now() > self.end_time


    @property
    def is_helper_profile_locked(self):
        return timezone.now() > self.helper_profile_lock_time

    
    def __str__(self):
        return 'Jumpstart'

    
    class Meta:
        verbose_name = 'Jumpstart'
        verbose_name_plural = 'Jumpstart'


class Group(models.Model):
    number = models.PositiveSmallIntegerField(unique=True, validators=[MinValueValidator(1)], verbose_name='Group Number')
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Group Name')


    def __str__(self):
        return 'Group {}'.format(self.number)


    class Meta:
        ordering = ['number']


class Fresher(models.Model):
    username = models.CharField(max_length=20, primary_key=True, verbose_name='Username')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='UUID')
    name = models.CharField(max_length=50, verbose_name='Name')
    preferred_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='preferred Name')
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='Group')
    is_checked_in = models.BooleanField(default=False, null=False, verbose_name='Checked In')


    def __str__(self):
        return self.username


    class Meta:
        ordering = ['group__number', 'name']


class Helper(models.Model):
    username = models.CharField(max_length=50, primary_key=True, verbose_name='Username')
    name = models.CharField(max_length=50, verbose_name='Name')
    preferred_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Preferred Name')
    photo = models.ImageField(upload_to=helper_photo_file_name, blank=True, validators=[validate_photo_file_extension], verbose_name='Photo')
    group = models.OneToOneField(Group, on_delete=models.PROTECT, verbose_name='Group')


    def __str__(self):
        return self.username


    class Meta:
        ordering = ['group__number']


class CharityShopChallengeSubmission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to=charity_shop_challenge_photo_file_name, validators=[validate_photo_file_extension], null=True, blank=True, verbose_name='Charity Shop Challenge Photo')


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
