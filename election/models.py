from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
import os


def nomination_image_file_name(instance, filename):
        return ('election/{}/{}-{}{}'.format(instance.position.election.codename, instance.username, uuid.uuid4(), os.path.splitext(filename)[1].lower()))


class DoesNotHaveNominationException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class Election(models.Model):
    codename = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, verbose_name='election name')
    voting_start = models.DateTimeField(verbose_name='voting start time', blank=False)
    voting_end = models.DateTimeField(verbose_name='voting end time', blank=False)
    has_nomination = models.BooleanField()
    nomination_start = models.DateTimeField(verbose_name='nomination start time', null=True, blank=True)
    nomination_end = models.DateTimeField(verbose_name='nomination end time', null=True, blank=True)


    @property
    def is_nomination_future(self):
        if self.has_nomination:
            return self.nomination_start > timezone.now()
        else:
            raise DoesNotHaveNominationException()

    @property
    def is_nomination_pase(self):
        if self.has_nomination:
            return self.nomination_end < timezone.now()
        else:
            raise DoesNotHaveNominationException()

    
    @property
    def is_nomination_current(self):
        return not (self.is_nomination_future or self.is_nomination_pase)


    @property
    def is_voting_future(self):
        return self.voting_start > timezone.now()
        


    @property
    def is_voting_past(self):
        return self.voting_end < timezone.now()

    
    @property
    def is_voting_current(self):
        return not (self.is_voting_future or self.is_voting_past)

    @property
    def is_election_current(self):
        if self.has_nomination:
            return self.nomination_start <= timezone.now() and self.voting_end >= timezone.now()
        else:
            return self.voting_start <= timezone.now() and self.voting_end >= timezone.now()

    
    def clean(self):
        if self.has_nomination and (not self.nomination_start or not self.nomination_end):
            raise ValidationError('Nomination must have a start and end time')
        elif not self.has_nomination and (self.nomination_start or self.nomination_end):
            raise ValidationError('Cannot set nomination start time and end time if this voting does not have a nomination')

        if self.has_nomination and self.nomination_start >= self.nomination_end:
            raise ValidationError('Nomination end time should not be the same or earlier than start time.')

        if self.voting_start >= self.voting_end:
            raise ValidationError('Voting end time should not be the same or earlier than start time.')

        if self.has_nomination and self.nomination_end > self.voting_start:
            raise ValidationError('Voting start time should not be earlier than nomination end time.')


    def __str__(self):
        return self.name


class Position(models.Model):
    codename = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, verbose_name='position name')
    election = models.ForeignKey(Election, on_delete=models.PROTECT)
    description = models.TextField(verbose_name='position description')
    sort_order = models.IntegerField(null=True, blank=True, verbose_name='position sort order')


class Nomination(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.PROTECT, verbose_name='nomination position')
    manifesto = models.TextField(verbose_name='nomination manifesto')
    photo = models.ImageField(upload_to=nomination_image_file_name)
    time = models.DateTimeField(auto_now=True)


class Support(models.Model):
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE)
    supporter = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now=True)
