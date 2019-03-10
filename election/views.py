from django.views import View
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.contrib import messages
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
import uuid

from .models import Election, Position, Nomination, Support
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


@login_required
def election(request, election):
    election = get_object_or_404(Election, codename=election)
    # do not show past election
    if election.voting_end < timezone.now():
        raise Http404

    context = {
        'election': election,
    }
    if is_nomination_current(election):
        return render(request, 'election/nomination.html', context)
    if is_voting_current(election):
        return HttpResponse('Voting')
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
        except Nomination.DoesNotExist:
            nomination_form = NominationForm(request.POST, request.FILES)
        nomination_form.fields['username'].initial = request.user.username
        nomination_form.fields['name'].initial = '{} {}'.format(request.user.first_name, request.user.last_name)
        if nomination_form.is_valid():
            nomination = nomination_form.save(commit=False)
            nomination.position = position
            nomination.save()
            messages.success(request, 'Your nomination for {} has been submitted.'.format(position.name))
            return redirect(to=reverse('election:election', args=[election.codename]))
        context = {
            'election': election,
            'position': position,
            'nomination_form': nomination_form,
        }
        return render(request, 'election/nominate.html', context)

@method_decorator(login_required, name='dispatch')
class SupportView(PermissionRequiredMixin, View):

    permission_required = 'ecsswebauth.is_ecs_user'
    raise_exception = True

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
