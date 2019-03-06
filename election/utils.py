from django.utils import timezone


def is_nomination_current(election):
    return election.has_nomination and election.nomination_start < timezone.now() and election.nomination_end > timezone.now()


def is_voting_current(election):
    return election.voting_start < timezone.now() and election.voting_end > timezone.now()
