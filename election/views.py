from django.views import View
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.contrib import messages
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.conf import settings
import uuid
import random
import yaml
import os

from .models import Election, Position, Nomination, Support, Voter, Vote, VoteRecord
from .forms import NominationForm
from .utils import is_nomination_current, is_voting_current


@login_required
def elections(request):
    # show all current and future elections for committee
    if request.user.groups.filter(name='committee').exists():
        elections = Election.objects.filter(voting_end__gte=timezone.now()).order_by('voting_start')
    else:
        current_elections_has_nomination = Election.objects.filter(Q(has_nomination=True) & Q(nomination_start__lte=timezone.now()) & Q(voting_end__gte=timezone.now()))
        current_elections_not_has_nomination = Election.objects.filter(Q(voting_start__lte=timezone.now()) & Q(voting_end__gte=timezone.now()))
        elections = (current_elections_has_nomination | current_elections_not_has_nomination).order_by('voting_start')
    context = {
        'elections': elections,
    }
    return render(request, 'election/elections.html', context)

def can_nominate(request):
    username = request.user.username

    with open('ecss_can_nominate.txt', 'r') as file:
        for line in file:
            if username in line:
                return True
    
    return request.user.has_perm('ecsswebauth.is_ecs_user')

def can_vote(request):
    username = request.user.username

    with open('ecss_can_vote.txt', 'r') as file:
        for line in file:
            if username in line:
                return True
    
    return request.user.has_perm('ecsswebauth.is_ecs_user')

@login_required
def election(request, election):
    election = get_object_or_404(Election, codename=election)
    # do not show past election
    if election.voting_end < timezone.now():
        raise Http404

    context = {
        'election': election,
        'can_nominate': can_nominate(request),
        'can_vote': can_vote(request)
    }
    if is_nomination_current(election):
        return render(request, 'election/nomination.html', context)
    if is_voting_current(election):
        return render(request, 'election/voting.html', context)
    if election.has_nomination and election.nomination_start <= timezone.now() and election.voting_end >= timezone.now():
        return render(request, 'election/election.html', context)
    if request.user.groups.filter(name='committee').exists():
        return render(request, 'election/election.html', context)
    else:
        raise Http404()



@method_decorator(login_required, name='dispatch')
class NominationView(PermissionRequiredMixin, View):

    permission_required = 'ecsswebauth.is_ecs_user'
    raise_exception = True

    def has_permission(self) -> bool:
        if super().has_permission():
            return True
    
        username = self.request.user.username

        with open('ecss_can_nominate.txt', 'r') as file:
            for line in file:
                if username in line:
                    return True
                
        return False

    def get(self, request, election, position):
        election = get_object_or_404(Election, codename=election)
        position = get_object_or_404(Position, codename=position, election=election)
        if not is_nomination_current(election):
            raise Http404()
        try:
            nomination = Nomination.objects.get(username=request.user.username, position=position)
            nomination_form = NominationForm(instance=nomination)
            support_shareable_link = '{}?nomination={}'.format(request.build_absolute_uri(reverse('website:election-support-shareable', args=[election.codename])), nomination.uuid)
        except Nomination.DoesNotExist:
            nomination_form = NominationForm(initial = {
                'username': request.user.username,
                'name': '{} {}'.format(request.user.first_name,     request.user.last_name)
            })
            support_shareable_link = None
        context = {
            'election': election,
            'position': position,
            'nomination_form': nomination_form,
            'support_shareable_link': support_shareable_link,
            'can_nominate': can_nominate(request),
            'can_vote': can_vote(request)
        }
        return render(request, 'election/nominate.html', context)

    def post(self, request, election, position):
        election = get_object_or_404(Election, codename=election)
        position = get_object_or_404(Position, codename=position, election=election)
        if not is_nomination_current(election):
            raise Http404()
        try:
            nomination = Nomination.objects.get(username=request.user.username, position=position)
            nomination_form = NominationForm(request.POST, request.FILES, instance=nomination)
            is_new = False
        except Nomination.DoesNotExist:
            nomination_form = NominationForm(request.POST, request.FILES)
            is_new = True
        nomination_form.fields['username'].initial = request.user.username
        nomination_form.fields['name'].initial = '{} {}'.format(request.user.first_name, request.user.last_name)
        if nomination_form.is_valid():
            nomination = nomination_form.save(commit=False)
            nomination.position = position
            nomination.save()
            messages.success(request, 'Your nomination for {} has been submitted.'.format(position.name))
            if is_new:
                name = nomination.nickname or nomination.name
                support_shareable_link = '{}?nomination={}'.format(request.build_absolute_uri(reverse('website:election-support-shareable', args=[election.codename])), nomination.uuid)
                nominate_link = request.build_absolute_uri(reverse('election:nomination', args=[election.codename, position.codename]))
                message_agm_2019 = 'Voting will be open shortly after the AGM. Come to the AGM on 17th March :)\n\nSee you there,\n'
                message = 'Hi {},\n\nThank you for your nomination for {} in {}.\n\nYou will need at least two members to support each of your nomination(s) before the nomination closes and you can share this link for others to support your nomination: {}.\n\nYou can modify your nomination at {} before nomination closes.\n\n{}ECSS\nhttps://society.ecs.soton.ac.uk'.format(name, position.name, election.name, support_shareable_link, nominate_link, message_agm_2019)
                EmailMessage(
                    '[ECSS] Nomination submitted for {} in {}'.format(position.name, election.name),
                    message,
                    'ECSS <no-reply@society.ecs.soton.ac.uk>',
                    [request.user.email],
                    reply_to = ['ECSS <society@ecs.soton.ac.uk>'],
                ).send(fail_silently=True)
            return redirect(to=reverse('election:election', args=[election.codename]))
        context = {
            'election': election,
            'position': position,
            'nomination_form': nomination_form,
            'can_nominate': can_nominate(request),
            'can_vote': can_vote(request)
        }
        return render(request, 'election/nominate.html', context)

@method_decorator(login_required, name='dispatch')
class SupportView(PermissionRequiredMixin, View):

    permission_required = 'ecsswebauth.is_ecs_user'
    raise_exception = True

    def has_permission(self) -> bool:
        if super().has_permission():
            return True
    
        username = self.request.user.username

        with open('ecss_can_vote.txt', 'r') as file:
            for line in file:
                if username in line:
                    return True
                
        return False

    def get(self, request, election, position):
        election = get_object_or_404(Election, codename=election)
        position = get_object_or_404(Position, codename=position, election=election)
        if not is_nomination_current(election):
            raise Http404()
        if not 'nomination' in request.GET:
            raise Http404()
        try:
            nomination = get_object_or_404(Nomination, uuid=request.GET['nomination'], position=position)
        except ValidationError:
            raise Http404()
        try:
            support = Support.objects.get(supporter=request.user.username, nomination__position=position)
            supporting_name = support.nomination.name
        except Support.DoesNotExist:
            supporting_name = None
        context = {
            'nomination': nomination,
            'supporting_name': supporting_name,
            'can_nominate': can_nominate(request),
            'can_vote': can_vote(request)
        }
        return render(request, 'election/support.html', context)

    def post(self, request, election, position):
        election = get_object_or_404(Election, codename=election)
        position = get_object_or_404(Position, codename=position, election=election)
        if not is_nomination_current(election):
            raise Http404()
        nomination = get_object_or_404(Nomination, uuid=request.POST['nomination'], position=position)
        
        try:
            support = Support.objects.get(nomination__position=position, supporter=request.user.username)
            support.nomination = nomination
            support.save()
        except Support.DoesNotExist:
            Support(nomination=nomination, supporter=request.user.username).save()

        if request.META['HTTP_ACCEPT'] == 'application/json':
            return JsonResponse({
                'status': 'success',
            })
        else:
            messages.success(request, 'You are supporting {} for {}.'.format(nomination.name, nomination.position.name))
            return redirect(to=reverse('election:election', args=[election.codename]))


@login_required
def support_shareable(request, election):
    response_404 = render(request, 'election/error-pages/nomination-404.html', status=404)
    election = get_object_or_404(Election, codename=election)
    if not is_nomination_current(election):
        return response_404
    if not 'nomination' in request.GET:
        raise Http404()
    try:
        try:
            nomination = Nomination.objects.get(uuid=request.GET['nomination'], position__election=election)
        except Nomination.DoesNotExist:
            return response_404
    except ValidationError:
        return response_404
    if not request.user.has_perm('ecsswebauth.is_ecs_user'):
        return render(request, 'election/error-pages/support-500.html', status=500)
    return redirect(to='{}?nomination={}'.format(reverse('election:support', args=[election.codename, nomination.position.codename]), nomination.uuid))


class PositionView(LoginRequiredMixin, View):

    def get(self, request, election, position):
        election = get_object_or_404(Election, codename=election)
        position = get_object_or_404(Position, election=election, codename=position)
        if not is_voting_current(election):
            raise Http404()
        nominations = list(position.nomination_set.all())
        random.shuffle(nominations)
        context = {
            'position': position,
            'nominations': nominations,
            'can_nominate': can_nominate(request),
            'can_vote': can_vote(request)
        }
        return render(request, 'election/position.html', context)


@method_decorator(login_required, name='dispatch')
class VoteView(PermissionRequiredMixin, View):

    permission_required = 'ecsswebauth.is_ecs_user'
    raise_exception = True

    def has_permission(self) -> bool:
        if super().has_permission():
            return True
    
        username = self.request.user.username

        with open('ecss_can_vote.txt', 'r') as file:
            for line in file:
                if username in line:
                    return True
                
        return False

    def post(self, request, election, position):
        election = get_object_or_404(Election, codename=election)
        position = get_object_or_404(Position, codename=position)
        if not is_voting_current(election):
            raise Http404()

        # check if the user has already voted for the position
        if Voter.objects.filter(username=request.user.username, position=position):
            messages.error(request, 'You have already voted for {} in {}'.format(position.name, election.name))
            return redirect(to=reverse('election:position', args=[election.codename, position.codename]))

        nominations_rank = dict.fromkeys([str(nomination.uuid) for nomination in position.nomination_set.all()])
        ranks = set(map(str, (range(1, len(nominations_rank) + 2))))

        # check if ranks are valid and unique, check if ron in has a valid rank
        has_ron = False
        for k, v in request.POST.items():
            if k == 'ron':
                if v in ranks:
                    ranks.remove(v)
                    has_ron = True
                else:
                    messages.error(request, 'Error. Your vote has not been recorded for {} in {}'.format(position.name, election.name))
                    return redirect(to=reverse('election:position', args=[election.codename, position.codename]))
            elif k in nominations_rank:
                if v in ranks:
                    nominations_rank[k] = int(v)
                    ranks.remove(v)
                else:
                    messages.error(request, 'Error. Your vote has not been recorded for {} in {}'.format(position.name, election.name))
                    return redirect(to=reverse('election:position', args=[election.codename, position.codename]))
        if not has_ron:
            messages.error(request, 'Error. Your vote has not been recorded for {} in {}'.format(position.name, election.name))
            return redirect(to=reverse('election:position', args=[election.codename, position.codename]))
        # check if all nominations for the position has a rank
        for _, v in nominations_rank.items():
            if v == None:
                messages.error(request, 'Error. Your vote has not been recorded for {} in {}'.format(position.name, election.name))
                return redirect(to=reverse('election:position', args=[election.codename, position.codename]))

        with transaction.atomic():
            Voter(username=request.user.username, position=position).save()
            vote = Vote(position=position)
            vote.save()
            for k, v in nominations_rank.items():
                nomination = Nomination.objects.get(uuid=k)
                VoteRecord(vote=vote, nomination=nomination, rank=v).save()

        messages.success(request, 'Your vote for {} in {} has been recorded'.format(position.name, election.name))

        return redirect(to=reverse('election:position', args=[election.codename, position.codename]))

@login_required
def results(request):
    try:
        with open(os.path.join(settings.BASE_DIR, 'election/data/agm2019.yaml')) as data_file:
            election = yaml.load(data_file)
    except:
        raise Http404()
    context = {
        'election': election,
    }
    return render(request, 'election/results.html', context)
