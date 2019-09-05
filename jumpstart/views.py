from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import Http404
from django.db import transaction
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.conf import settings

from .models import Fresher, Helper, Group, CityChallengeScoreAuditlog

from .forms import HelperEditProfileForm, EditCityChallengeForm, EditScavengerHuntForm, ScoreMitreChallengeForm, ScoreCodingChallengeForm, ScoreStagsQuizForm, ScoreGamesChallengeForm, ScoreSportsChallengeForm

from .utils import jumpstart_check, is_fresher, is_helper

from website.utils import is_committee

from auditlog.models import AuditLog

import os
import requests
import json
import base64


@method_decorator(login_required, name='dispatch')
class HomeView(UserPassesTestMixin, View):


    raise_exception = True


    def test_func(self):
        return jumpstart_check(self.request.user)


    def get(self, request):
        if is_fresher(request.user):
            fresher = Fresher.objects.get(pk=request.user.username)
            groups = Group.objects.all().order_by('id')
            context = {
                'fresher': fresher,
                'groups': groups,
            }
            return render(request, 'jumpstart/fresher.html', context)
        elif is_helper(request.user):
            jumpstart = get_current_site(request).jumpstart
            helper = Helper.objects.get(pk=request.user.username)
            num_checked_in_group_members = helper.group.fresher_set.filter(is_checked_in=True).count()
            info = open(os.path.join(settings.BASE_DIR, 'jumpstart/data/helper-info.md'), 'r').read()
            context = {
                'jumpstart': jumpstart,
                'helper': helper,
                'num_checked_in_group_members': num_checked_in_group_members,
                'info': info,
            }
            return render(request, 'jumpstart/helper-jumpstart.html', context)
        elif is_committee(request.user):
            groups = Group.objects.all().order_by('id')
            context = {
                'groups': groups,
            }
            return render(request, 'jumpstart/committee.html', context)
        else:
            raise PermissionDenied()


'''
Show group and member info for helpers.
'''
@method_decorator(login_required, name='dispatch')
class HelperGroupView(UserPassesTestMixin, View):


    raise_exception = True


    def test_func(self):
        return is_helper(self.request.user)


    def get(self, request):
        helper = Helper.objects.get(pk=request.user.username)
        group_members = helper.group.fresher_set
        num_checked_in_group_members = group_members.filter(is_checked_in=True).count()
        group_members_uuid_json = json.dumps(list(map(str, group_members.all().values_list('uuid', flat=True))))
        group_members_uuid_serialized = base64.urlsafe_b64encode(group_members_uuid_json.encode()).decode('utf-8')
        context = {
            'helper': helper,
            'num_checked_in_group_members': num_checked_in_group_members,
            'group_members_uuid_serialized': group_members_uuid_serialized,
        }
        return render(request, 'jumpstart/helper-group.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileEditView(UserPassesTestMixin, View):

    raise_exception = True

    def test_func(self):
        return jumpstart_check(self.request.user)

    def get(self, request):
        if is_fresher(request.user):
            raise Http404()
        elif is_helper(request.user):
            helper = Helper.objects.get(pk=request.user.username)
            profile_edit_form = HelperEditProfileForm(instance=helper)
            context = {
                'profile_edit_form': profile_edit_form,
            }
            return render(request, 'jumpstart/helper-profile-edit.html', context)
        else:
            raise Http404()

    def post(self, request):
        if is_fresher(request.user):
            raise Http404()
        elif is_helper(request.user):
            helper = Helper.objects.get(pk=request.user.username)

            profile_edit_form = HelperEditProfileForm(request.POST, request.FILES, instance=helper)

            if profile_edit_form.is_valid():
                profile_edit_form.save()
                message = 'Your profile has been updated successfully.'

                if 'photo' in profile_edit_form.changed_data and settings.FACE_DETECT_ENABLED:
                    files = {
                        'image': helper.photo.file,
                    }
                    response = requests.post(settings.FACE_DETECT_API, files=files)
                    if response.status_code == 200:
                        response = json.loads(response.text)
                        if response['num_faces'] == 1:
                            message += ' Nice photo!'
                        elif response['num_faces'] > 1:
                            messages.warning(request, 'How many people are there in the photo? (Face detection is an experimental feature)')
                        else:
                            messages.warning(request, 'Are you in the picture? (Face detection is an experimental feature)')

                messages.success(request, message)
                return redirect('jumpstart:home')

            context = {
                'profile_edit_form': profile_edit_form,
            }
            return render(request, 'jumpstart/helper-profile-edit.html', context)
        else:
            raise Http404()

@method_decorator(login_required, name='dispatch')
class CityChallengeEditView(UserPassesTestMixin, View):
    
    raise_exception = True

    def test_func(self):
        return jumpstart_check(self.request.user)

    def get(self, request):
        if is_committee(request.user):
            raise Http404()
        elif is_helper(request.user):
            group = Group.objects.get(helper=request.user.username)
            city_challenge_edit_form = EditCityChallengeForm(instance=group)
            context = {
                'group': group,
                'city_challenge_edit_form': city_challenge_edit_form,
            }
            return render(request, 'jumpstart/city-challenge-edit.html', context)
        else:
            raise Http404()

    def post(self, request):
        if is_committee(request.user):
            raise Http404()
        elif is_helper(request.user):
            group = Group.objects.get(helper=request.user.username)

            city_challenge_edit_form = EditCityChallengeForm(request.POST, request.FILES, instance=group)

            if city_challenge_edit_form.is_valid():
                city_challenge_edit_form.save()
                messages.success(request, 'Your group\'s City Challenge has been updated successfully.')
                return redirect('jumpstart:home')

            context = {
                'group': group,
                'city_challenge_edit_form': city_challenge_edit_form,
            }
            return render(request, 'jumpstart/city-challenge-edit.html', context)
        else:
            raise Http404()


@method_decorator(login_required, name='dispatch')
class ScavengerHuntView(UserPassesTestMixin, View):

    raise_exception = True

    def test_func(self):
        return jumpstart_check(self.request.user)

    def get(self, request):
        if is_fresher(request.user):
            group = Fresher.objects.get(pk=request.user.username).group
        elif is_helper(request.user):
            group = Group.objects.get(helper=request.user.username)
        elif is_committee(request.user):
            groups = Group.objects.all().order_by('id')
            context = {
                'groups': groups,
            }
            return render(request, 'jumpstart/scavenger-hunt-all.html', context)
        else:
            raise PermissionDenied()

        context = {
            'group': group,
        }
        return render(request, 'jumpstart/scavenger-hunt.html', context)


@method_decorator(login_required, name='dispatch')
class ScavengerHuntEditView(UserPassesTestMixin, View):

    raise_exception = True

    def test_func(self):
        return jumpstart_check(self.request.user)

    def get(self, request):
        if is_fresher(request.user):
            raise PermissionDenied()
        elif is_helper(request.user):
            group = Group.objects.get(helper=request.user.username)
            scavenger_hunt_edit_form = EditScavengerHuntForm()
            context = {
                'group': group,
                'scavenger_hunt_edit_form': scavenger_hunt_edit_form,
            }
            return render(request, 'jumpstart/scavenger-hunt-edit.html', context)
        else:
            raise Http404()

    def post(self, request):
        if is_fresher(request.user):
            raise PermissionDenied()
        elif is_helper(request.user):
            group = Group.objects.get(helper=request.user.username)

            scavenger_hunt_edit_form = EditScavengerHuntForm(request.POST, request.FILES)

            if scavenger_hunt_edit_form.is_valid():
                scavenger_hunt = scavenger_hunt_edit_form.save(commit=False)
                scavenger_hunt.group = Group.objects.get(helper=request.user.username)
                scavenger_hunt.save()
                messages.success(request, '1 image has been uploaded for Scavenger Hunt successfully.')
                return redirect('jumpstart:scavenger-hunt-edit')

            context = {
                'group': group,
                'scavenger_hunt_edit_form': scavenger_hunt_edit_form,
            }
            return render(request, 'jumpstart/scavenger-hunt-edit.html', context)
        else:
            raise Http404()


@method_decorator(login_required, name='dispatch')
class GroupsView(UserPassesTestMixin, View):

    raise_exception = True

    def test_func(self):
        return jumpstart_check(self.request.user)

    def get(self, request):
        if is_fresher(request.user):
            groups = Group.objects.all().order_by('id')
            context = {
                'groups': groups,
            }
            return render(request, 'jumpstart/groups.html', context)
        elif is_helper(request.user):
            groups = Group.objects.all().order_by('id')
            context = {
                'groups': groups,
            }
            return render(request, 'jumpstart/groups.html', context)
        else:
            raise Http404()


@method_decorator(login_required, name='dispatch')
class CityChallengeView(UserPassesTestMixin, View):

    raise_exception = True

    def test_func(self):
        return is_committee(self.request.user)

    def get(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        score_mitre_challenge_form = ScoreMitreChallengeForm(instance=group)
        score_coding_challenge_form = ScoreCodingChallengeForm(instance=group)
        stags_quiz_score_form = ScoreStagsQuizForm(instance=group)
        games_challenge_score_form = ScoreGamesChallengeForm(instance=group)
        sports_challenge_score_form = ScoreSportsChallengeForm(instance=group)
        context = {
            'forms': [
                    (score_mitre_challenge_form, 'mitre'),
                    (score_coding_challenge_form, 'coding'),
                    (stags_quiz_score_form, 'stags'),
                    (games_challenge_score_form, 'games'),
                    (sports_challenge_score_form, 'sports'),
                ],
            'group': group,
        }
        return render(request, 'jumpstart/city-challenge.html', context)

    def post(self, request, group_id):
        if 'challenge' not in request.GET:
            raise Http404()

        group = get_object_or_404(Group, pk=group_id)

        if request.GET.get('challenge') == 'mitre':
            form = ScoreMitreChallengeForm(request.POST, instance=group)
        elif request.GET.get('challenge') == 'coding':
            form = ScoreCodingChallengeForm(request.POST, instance=group)
        elif request.GET.get('challenge') == 'stags':
            form = ScoreStagsQuizForm(request.POST, instance=group)
        elif request.GET.get('challenge') == 'games':
            form = ScoreGamesChallengeForm(request.POST, instance=group)
        elif request.GET.get('challenge') == 'sports':
            form = ScoreSportsChallengeForm(request.POST, instance=group)
        else:
            raise Http404()
        
        if form.is_valid():
            form.save()
            challenges = {
                'mitre': 'Mitre Challenge',
                'coding': 'Coding Challenge',
                'stags': 'Stags Quiz',
                'games': 'Games Challenge',
                'sports': 'Sports Challenge',
            }

            if request.GET.get('challenge') == 'mitre':
                score = group.mitre_challenge_score
            elif request.GET.get('challenge') == 'coding':
                score = group.coding_challenge_score
            elif request.GET.get('challenge') == 'stags':
                score = group.stags_quiz_score
            elif request.GET.get('challenge') == 'games':
                score = group.games_challenge_score
            elif request.GET.get('challenge') == 'sports':
                score = group.sports_challenge_score

            city_challenge_score_auditlog = CityChallengeScoreAuditlog.objects.create(user=request.user.username, group=group, challenge=challenges[request.GET.get('challenge')], score=score)
            AuditLog.objects.create(content_object=city_challenge_score_auditlog)

            messages.success(request, 'You have updated score of {} for Group {}'.format(challenges[request.GET.get('challenge')], group.id))
            return redirect(reverse_lazy('jumpstart:city-challenge', kwargs={'group_id': group.id}))
        else:
            score_mitre_challenge_form = ScoreMitreChallengeForm(instance=group)
            score_coding_challenge_form = ScoreCodingChallengeForm(instance=group)
            stags_quiz_score_form = ScoreStagsQuizForm(instance=group)
            games_challenge_score_form = ScoreGamesChallengeForm(instance=group)
            sports_challenge_score_form = ScoreSportsChallengeForm(instance=group)

            if request.GET.get('challenge') == 'mitre':
                score_mitre_challenge_form = form
            elif request.GET.get('challenge') == 'coding':
                score_coding_challenge_form = form
            elif request.GET.get('challenge') == 'stags':
                stags_quiz_score_form = form
            elif request.GET.get('challenge') == 'games':
                games_challenge_score_form = form
            elif request.GET.get('challenge') == 'sports':
                sports_challenge_score_form = form

            context = {
                'forms': [
                    (score_mitre_challenge_form, 'mitre'),
                    (score_coding_challenge_form, 'coding'),
                    (stags_quiz_score_form, 'stags'),
                    (games_challenge_score_form, 'games'),
                    (sports_challenge_score_form, 'sports'),
                ],
                'group': group,
            }
        return render(request, 'jumpstart/city-challenge.html', context)


'''
Update freshers' check in status.
'''
@method_decorator(login_required, name='dispatch')
class MemberCheckInView(UserPassesTestMixin, View):


    raise_exception = True


    def test_func(self):
        return is_helper(self.request.user)


    def post(self, request):
        helper = Helper.objects.get(pk=request.user.username)
        # check if update is allowed
        group_members = helper.group.fresher_set.all()
        group_members_uuid = set(map(str, group_members.values_list('uuid', flat=True)))
        try:
            members_uuid_base64 = request.POST['group_members']
            members_uuid_json = base64.urlsafe_b64decode(members_uuid_base64.encode()).decode('utf-8')
            members_uuid = set(json.loads(members_uuid_json))
            if members_uuid.issubset(group_members_uuid):
                # update check in status
                with transaction.atomic():
                    for member_uuid in members_uuid:
                        member = Fresher.objects.get(uuid=member_uuid)
                        if member_uuid in request.POST:
                            member.is_checked_in = True
                        else:
                            member.is_checked_in = False
                        member.save()
                    messages.success(request, 'Successfully updated members check in status.')
            else:
                messages.error(request, 'Permission denined. Failed to update.')
        except:
            messages.error(request, 'An error occurred. Failed to update.')
        return redirect('jumpstart:group')
