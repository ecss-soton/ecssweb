from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.db import transaction
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.conf import settings

from .models import Fresher, Helper, Group, CityChallengeScoreAuditlog

from .forms import HelperProfileEditForm, FresherProfileEditForm, EditGroupNameForm, SubmitCharityShopChallengeForm, EditScavengerHuntForm

from .utils import jumpstart_check, is_fresher, is_helper

from website.utils import is_committee

from auditlog.models import AuditLog

from io import StringIO
import os
import requests
import json
import csv
import base64


@method_decorator(login_required, name='dispatch')
class HomeView(UserPassesTestMixin, View):
    """Jumpstart portal homepage for freshers, helpers and committee."""

    raise_exception = True


    def test_func(self):
        """Only people involved in Jumpstart have access."""
        return jumpstart_check(self.request.user)


    def get(self, request):
        if is_fresher(request.user):
            return self._get_fresher(request)
        elif is_helper(request.user):
            return self._get_helper(request)
        elif is_committee(request.user):
            return self._get_committee(request)
        else:
            raise PermissionDenied()


    def _get_fresher(self, request):
        """Render page for freshers."""
        jumpstart = get_current_site(request).jumpstart
        fresher = Fresher.objects.get(pk=request.user.username)
        context = {
            'jumpstart': jumpstart,
            'fresher': fresher,
        }
        return render(request, 'jumpstart/fresher-jumpstart.html', context)


    def _get_helper(self, request):
        """Render page for helpers."""
        jumpstart = get_current_site(request).jumpstart
        helper = Helper.objects.get(pk=request.user.username)
        info = open(os.path.join(settings.BASE_DIR, 'jumpstart/data/helper-info.md'), 'r').read()
        context = {
            'jumpstart': jumpstart,
            'helper': helper,
            'info': info,
        }
        return render(request, 'jumpstart/helper-jumpstart.html', context)


    def _get_committee(self, request):
        """Render page for committee."""
        context = {

        }
        return render(request, 'jumpstart/committee-jumpstart.html', context)


@method_decorator(login_required, name='dispatch')
class GroupView(UserPassesTestMixin, View):
    """Show group info for helpers and freshers."""

    raise_exception = True


    def test_func(self):
        """Only helpers and freshers have access to group page for their own group."""
        return  is_helper(self.request.user) or is_fresher(self.request.user)


    def get(self, request):
        if is_helper(self.request.user):
            return self._get_helper(request)
        elif is_fresher(self.request.user):
            return self._get_fresher(request)
        else:
            raise PermissionDenied()


    def _get_helper(self, request):
        """Render page for helpers."""
        jumpstart = get_current_site(request).jumpstart
        helper = Helper.objects.get(pk=request.user.username)
        group_members = helper.group.fresher_set
        group_members_uuid_json = json.dumps(list(map(str, group_members.all().values_list('uuid', flat=True))))
        group_members_uuid_serialized = base64.urlsafe_b64encode(group_members_uuid_json.encode()).decode('utf-8')
        context = {
            'jumpstart': jumpstart,
            'helper': helper,
            'group_members_uuid_serialized': group_members_uuid_serialized,
        }
        return render(request, 'jumpstart/helper-group.html', context)


    def _get_fresher(self, request):
        """Render page for freshers."""
        fresher = Fresher.objects.get(pk=request.user.username)
        context = {
            'fresher': fresher,
        }
        return render(request, 'jumpstart/fresher-group.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileView(UserPassesTestMixin, View):
    """Show helpers and freshers their profile and allow edit if profile is unlocked."""

    raise_exception = True


    def test_func(self):
        """Only helpers and freshers have access to this view."""
        return is_helper(self.request.user) or is_fresher(self.request.user)


    def get(self, request):
        if is_helper(request.user):
            return self._get_helper(request)
        elif is_fresher(request.user):
            return self._get_fresher(request)
        else:
            raise PermissionDenied()


    def _get_helper(self, request):
        """Render page for helpers."""
        # Check if helpers profile is locked
        jumpstart = get_current_site(request).jumpstart
        if jumpstart.is_helper_profile_locked:
            # Render view only if profile is locked
            helper = Helper.objects.get(pk=request.user.username)
            context = {
                'helper': helper,
            }
            return render(request, 'jumpstart/helper-profile.html', context)
        else:
            # Render edit form if profile is unlocked
            helper = Helper.objects.get(pk=request.user.username)
            profile_edit_form = HelperProfileEditForm(instance=helper)
            context = {
                'helper': helper,
                'profile_edit_form': profile_edit_form,
            }
            return render(request, 'jumpstart/helper-profile-edit.html', context)


    def _get_fresher(self, request):
        """Render page for freshers."""
        # Check if freshers profile is locked
        jumpstart = get_current_site(request).jumpstart
        if jumpstart.is_after:
            # Render view only if profile is locked
            fresher = Fresher.objects.get(pk=request.user.username)
            context = {
                'fresher': fresher,
            }
            return render(request, 'jumpstart/fresher-profile.html', context)
        else:
            # Render edit form if profile is unlocked
            fresher = Fresher.objects.get(pk=request.user.username)
            profile_edit_form = FresherProfileEditForm(instance=fresher)
            context = {
                'profile_edit_form': profile_edit_form,
            }
            return render(request, 'jumpstart/fresher-profile-edit.html', context)


    def post(self, request):
        if is_helper(request.user):
            return self._post_helper(request)
        elif is_fresher(request.user):
            return self._post_fresher(request)
        else:
            raise PermissionDenied()


    def _post_helper(self, request):
        # Check if helpers profile is unlocked
        jumpstart = get_current_site(request).jumpstart
        if jumpstart.is_helper_profile_locked:
            messages.error('Your profile is locked. Failed to update your profile.')
            return redirect('jumpstart:home')
        # Validate form and update profile
        helper = Helper.objects.get(pk=request.user.username)
        profile_edit_form = HelperProfileEditForm(request.POST, request.FILES, instance=helper)
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            messages.success(request, 'Successfully updated your profile.')
            return redirect('jumpstart:home')
        # Show edit form again if form was not valid
        helper = Helper.objects.get(pk=request.user.username) # Retrieve the instance from the database to render the page with valid data 
        context = {
            'helper': helper,
            'profile_edit_form': profile_edit_form,
        }
        return render(request, 'jumpstart/helper-profile-edit.html', context)


    def _post_fresher(self, request):
        # Check if freshers profile is unlocked
        jumpstart = get_current_site(request).jumpstart
        if jumpstart.is_after:
            messages.error('Your profile is locked. Failed to update your profile.')
            return redirect('jumpstart:home')
        # Validate form and update profile
        fresher = Fresher.objects.get(pk=request.user.username)
        profile_edit_form = FresherProfileEditForm(request.POST, instance=fresher)
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            messages.success(request, 'Successfully updated your profile.')
            return redirect('jumpstart:home')
        # Show edit form again if form was not valid
        context = {
            'profile_edit_form': profile_edit_form,
        }
        return render(request, 'jumpstart/fresher-profile-edit.html', context)


@method_decorator(login_required, name='dispatch')
class FresherGroupHelperView(UserPassesTestMixin, View):
    """Show group helper for freshers."""

    raise_exception = True


    def test_func(self):
        """Only freshers have access."""
        return is_fresher(self.request.user)


    def get(self, request):
        fresher = Fresher.objects.get(pk=request.user.username)
        context = {
            'fresher': fresher,
        }
        return render(request, 'jumpstart/fresher-group-helper.html', context)


@method_decorator(login_required, name='dispatch')
class CommitteeGroupsView(UserPassesTestMixin, View):
    """Show Jumpstart groups for committee."""

    raise_exception = True


    def test_func(self):
        """Only committee have access."""
        return is_committee(self.request.user)

    
    def get(self, request):
        jumpstart = get_current_site(request).jumpstart
        groups = Group.objects.all().order_by('number')
        is_show_helper_photos = request.GET.get('show_helper_photos', False) == 'yes'
        is_show_members = request.GET.get('show_members', False) == 'yes'
        context = {
            'jumpstart': jumpstart,
            'groups': groups,
            'is_show_helper_photos': is_show_helper_photos,
            'is_show_members': is_show_members,
        }
        return render(request, 'jumpstart/committee-groups.html', context)


@method_decorator(login_required, name='dispatch')
class CommitteeGroupView(UserPassesTestMixin, View):
    """Show Jumpstart group for committee."""

    raise_exception = True


    def test_func(self):
        """Only committee have access."""
        return is_committee(self.request.user)

    
    def get(self, request, group_number):
        jumpstart = get_current_site(request).jumpstart
        group = Group.objects.get(number=group_number)
        context = {
            'jumpstart': jumpstart,
            'group': group,
        }
        return render(request, 'jumpstart/committee-group.html', context)


@method_decorator(login_required, name='dispatch')
class CommitteeGroupsImportExportView(UserPassesTestMixin, View):
    """Show groups helpers and freshers import and export for committee."""

    raise_exception = True


    def test_func(self):
        """Only committee have access."""
        return is_committee(self.request.user)

    
    def get(self, request):
        return render(request, 'jumpstart/committee-groups-import-export.html')


@method_decorator(login_required, name='dispatch')
class CommitteeGroupsHelpersExportView(UserPassesTestMixin, View):
    """Export CSV file of groups helpers for committee, with columns of group number, username, name, preferred name and photo file."""

    raise_exception = True


    def test_func(self):
        """Only committee have access."""
        return is_committee(self.request.user)

    
    def get(self, request):
        helpers = Helper.objects.all().order_by('group__number')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="helpers.csv"'
        csv_writer = csv.writer(response)
        csv_writer.writerow(['group_number', 'username', 'name', 'preferred_name', 'photo_file'])
        for helper in helpers:
            csv_writer.writerow([helper.group.number, helper.username, helper.name, helper.preferred_name, helper.photo])
        return response


@method_decorator(login_required, name='dispatch')
class CommitteeGroupsFreshersExportView(UserPassesTestMixin, View):
    """Export CSV file of freshers for committee, with columns of group number, username, name, preferred name and if checked in."""

    raise_exception = True


    def test_func(self):
        """Only committee have access."""
        return is_committee(self.request.user)

    
    def get(self, request):
        freshers = Fresher.objects.all().order_by('group__number', 'name')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="freshers.csv"'
        csv_writer = csv.writer(response)
        csv_writer.writerow(['group_number', 'username', 'name', 'preferred_name', 'is_checked_in'])
        for fresher in freshers:
            csv_writer.writerow([fresher.group.number, fresher.username, fresher.name, fresher.preferred_name, fresher.is_checked_in])
        return response


@method_decorator(login_required, name='dispatch')
class CommitteeGroupsHelpersImportView(UserPassesTestMixin, View):
    """Import helpers from a CSV file for committee.
       The CSV file has columns of group number, username, name, preferred name (optional) and photo file (optional).
       POST method only.
    """

    raise_exception = True


    def test_func(self):
        """Only webmaster has access."""
        return self.request.user.is_superuser

    
    def post(self, request):
        # Check if there are any helpers in the database. Abort if so
        if Helper.objects.all().count() > 0:
            messages.error(request, 'There are helpers in the database. Must be a new setup to import. Did not import.')
            return redirect('jumpstart:groups-import-export')
        helpers_file = request.FILES['helpers_file']
        helpers_file = StringIO(helpers_file.read().decode())
        csv_reader = csv.DictReader(helpers_file)
        try:
            num_helpers = 0
            num_new_groups = 0
            with transaction.atomic():
                for row in csv_reader:
                    # Get data from each row
                    group_number = int(row['group_number'])
                    username = row['username']
                    name = row['name']
                    preferred_name = row.get('preferred_name', None)
                    photo_file = row.get('photo_file', None)
                    # Create instances
                    group, created = Group.objects.get_or_create(number=group_number)
                    if created:
                        num_new_groups += 1
                    helper = Helper.objects.create(username=username, name=name, group=group, preferred_name=preferred_name, photo=photo_file)
                    helper.save()
                    num_helpers += 1
                messages.success(request, 'Successfully imported {} helper(s). {} new group(s) created.'.format(num_helpers, num_new_groups))
        except Exception as e:
            print(e)
            messages.error(request, 'Error occurred. Failed to import.')
        return redirect('jumpstart:groups-import-export')


@method_decorator(login_required, name='dispatch')
class CommitteeGroupsFreshersImportView(UserPassesTestMixin, View):
    """Import freshers from a CSV file for committee.
       The CSV file has columns of group number, username, name, preferred name (optional) and if checked in (default False).
       POST method only.
    """

    raise_exception = True


    def test_func(self):
        """Only webmaster has access."""
        return self.request.user.is_superuser

    
    def post(self, request):
        # Check if there are any freshers in the database. Abort if so
        if Fresher.objects.all().count() > 0:
            messages.error(request, 'There are freshers in the database. Must be a new setup to import. Did not import.')
            return redirect('jumpstart:groups-import-export')
        freshers_file = request.FILES['freshers_file']
        freshers_file = StringIO(freshers_file.read().decode())
        csv_reader = csv.DictReader(freshers_file)
        try:
            num_freshers = 0
            num_new_groups = 0
            with transaction.atomic():
                for row in csv_reader:
                    # Get data from each row
                    group_number = int(row['group_number'])
                    username = row['username']
                    name = row['name']
                    preferred_name = row.get('preferred_name', None)
                    is_checked_in = row.get('is_checked_in', False)
                    # Create instances
                    group, created = Group.objects.get_or_create(number=group_number)
                    if created:
                        num_new_groups += 1
                    fresher = Fresher.objects.create(username=username, name=name, group=group, preferred_name=preferred_name, is_checked_in=is_checked_in)
                    fresher.save()
                    num_freshers += 1
                messages.success(request, 'Successfully imported {} fresher(s). {} new group(s) created.'.format(num_freshers, num_new_groups))
        except Exception as e:
            print(e)
            messages.error(request, 'Error occurred. Failed to import.')
        return redirect('jumpstart:groups-import-export')


@method_decorator(login_required, name='dispatch')
class CityChallengeView(UserPassesTestMixin, View):
    """Show City Challenge for freshers and helpers and allow helpers to submit during the event."""
    
    raise_exception = True

    def test_func(self):
        """Only freshers and helpers have access to this view."""
        return is_fresher(self.request.user) or is_helper(self.request.user)

    def get(self, request):
        if is_fresher(request.user):
            return self._get_fresher(request)
        elif is_helper(request.user):
            return self._get_helper(request)
        else:
            raise PermissionDenied()


    def _get_fresher(self, request):
        """Render page for freshers."""
        fresher = Fresher.objects.get(username=request.user.username)
        group = fresher.group
        context = {
            'group': group,
        }
        return render(request, 'jumpstart/fresher-city-challenge.html', context)


    def _get_helper(self, request):
        """Render page for helpers."""
        # Check if is during the event
        jumpstart = get_current_site(request).jumpstart
        if jumpstart.is_now:
            # Render submission forms if during the event
            group = Group.objects.get(helper=request.user.username)
            edit_group_name_form = EditGroupNameForm(instance=group)
            submit_charity_shop_challenge_form = SubmitCharityShopChallengeForm()
            context = {
                'group': group,
                'edit_group_name_form': edit_group_name_form,
                'submit_charity_shop_challenge_form': submit_charity_shop_challenge_form,
            }
            return render(request, 'jumpstart/helper-city-challenge-edit.html', context)
        else:
            # Render view only if not during the event
            group = Group.objects.get(helper=request.user.username)
            context = {
                'group': group,
            }
            return render(request, 'jumpstart/helper-city-challenge.html', context)


    def post(self, request):
        if is_helper(request.user):
            action = request.POST.get('action', None)
            if action == 'update_group_name':
                return self._helper_update_group_name_post(request)
            elif action == 'submit_charity_shop_challenge':
                return self._helper_submit_charity_shop_challenge_post(request)
            else:
                return HttpResponseBadRequest()
        else:
            raise PermissionDenied()


    def _helper_update_group_name_post(self, request):
        jumpstart = get_current_site(request).jumpstart
        if not jumpstart.is_now:
            messages.error(request, 'Group name can only be updated during the event. Failed to update group name.')
            return redirect('jumpstart:city-challenge')
        else:
            group = Group.objects.get(helper=request.user.username)
            edit_group_name_form = EditGroupNameForm(request.POST, instance=group)
            if edit_group_name_form.is_valid():
                edit_group_name_form.save()
                messages.success(request, 'Successfully updated your group name.')
                return redirect('jumpstart:city-challenge')
            submit_charity_shop_challenge_form = SubmitCharityShopChallengeForm()
            context = {
                'group': group,
                'edit_group_name_form': edit_group_name_form,
                'submit_charity_shop_challenge_form': submit_charity_shop_challenge_form,
            }
            return render(request, 'jumpstart/helper-city-challenge-edit.html', context)


    def _helper_submit_charity_shop_challenge_post(self, request):
        jumpstart = get_current_site(request).jumpstart
        if not jumpstart.is_now:
            messages.error(request, 'Submission to Charity Shop Challenge can only be done during the event. Failed to submit to Charity Shop Challenge.')
            return redirect('jumpstart:city-challenge')
        else:
            submit_charity_shop_challenge_form = SubmitCharityShopChallengeForm(request.POST, request.FILES)
            group = Group.objects.get(helper=request.user.username)
            if submit_charity_shop_challenge_form.is_valid():
                charity_shop_challenge_submission = submit_charity_shop_challenge_form.save(commit=False)
                charity_shop_challenge_submission.group = group
                charity_shop_challenge_submission.save()
                messages.success(request, 'Successfully submitted to Charity Shop Challenge.')
                return redirect('jumpstart:city-challenge')
            edit_group_name_form = EditGroupNameForm()
            context = {
                'group': group,
                'edit_group_name_form': edit_group_name_form,
                'submit_charity_shop_challenge_form': submit_charity_shop_challenge_form,
            }
            return render(request, 'jumpstart/helper-city-challenge-edit.html', context)


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


# @method_decorator(login_required, name='dispatch')
# class CityChallengeView(UserPassesTestMixin, View):

#     raise_exception = True

#     def test_func(self):
#         return is_committee(self.request.user)

#     def get(self, request, group_id):
#         group = get_object_or_404(Group, pk=group_id)
#         score_mitre_challenge_form = ScoreMitreChallengeForm(instance=group)
#         score_coding_challenge_form = ScoreCodingChallengeForm(instance=group)
#         stags_quiz_score_form = ScoreStagsQuizForm(instance=group)
#         games_challenge_score_form = ScoreGamesChallengeForm(instance=group)
#         sports_challenge_score_form = ScoreSportsChallengeForm(instance=group)
#         context = {
#             'forms': [
#                     (score_mitre_challenge_form, 'mitre'),
#                     (score_coding_challenge_form, 'coding'),
#                     (stags_quiz_score_form, 'stags'),
#                     (games_challenge_score_form, 'games'),
#                     (sports_challenge_score_form, 'sports'),
#                 ],
#             'group': group,
#         }
#         return render(request, 'jumpstart/city-challenge.html', context)

#     def post(self, request, group_id):
#         if 'challenge' not in request.GET:
#             raise Http404()

#         group = get_object_or_404(Group, pk=group_id)

#         if request.GET.get('challenge') == 'mitre':
#             form = ScoreMitreChallengeForm(request.POST, instance=group)
#         elif request.GET.get('challenge') == 'coding':
#             form = ScoreCodingChallengeForm(request.POST, instance=group)
#         elif request.GET.get('challenge') == 'stags':
#             form = ScoreStagsQuizForm(request.POST, instance=group)
#         elif request.GET.get('challenge') == 'games':
#             form = ScoreGamesChallengeForm(request.POST, instance=group)
#         elif request.GET.get('challenge') == 'sports':
#             form = ScoreSportsChallengeForm(request.POST, instance=group)
#         else:
#             raise Http404()
        
#         if form.is_valid():
#             form.save()
#             challenges = {
#                 'mitre': 'Mitre Challenge',
#                 'coding': 'Coding Challenge',
#                 'stags': 'Stags Quiz',
#                 'games': 'Games Challenge',
#                 'sports': 'Sports Challenge',
#             }

#             if request.GET.get('challenge') == 'mitre':
#                 score = group.mitre_challenge_score
#             elif request.GET.get('challenge') == 'coding':
#                 score = group.coding_challenge_score
#             elif request.GET.get('challenge') == 'stags':
#                 score = group.stags_quiz_score
#             elif request.GET.get('challenge') == 'games':
#                 score = group.games_challenge_score
#             elif request.GET.get('challenge') == 'sports':
#                 score = group.sports_challenge_score

#             city_challenge_score_auditlog = CityChallengeScoreAuditlog.objects.create(user=request.user.username, group=group, challenge=challenges[request.GET.get('challenge')], score=score)
#             AuditLog.objects.create(content_object=city_challenge_score_auditlog)

#             messages.success(request, 'You have updated score of {} for Group {}'.format(challenges[request.GET.get('challenge')], group.id))
#             return redirect(reverse_lazy('jumpstart:city-challenge', kwargs={'group_id': group.id}))
#         else:
#             score_mitre_challenge_form = ScoreMitreChallengeForm(instance=group)
#             score_coding_challenge_form = ScoreCodingChallengeForm(instance=group)
#             stags_quiz_score_form = ScoreStagsQuizForm(instance=group)
#             games_challenge_score_form = ScoreGamesChallengeForm(instance=group)
#             sports_challenge_score_form = ScoreSportsChallengeForm(instance=group)

#             if request.GET.get('challenge') == 'mitre':
#                 score_mitre_challenge_form = form
#             elif request.GET.get('challenge') == 'coding':
#                 score_coding_challenge_form = form
#             elif request.GET.get('challenge') == 'stags':
#                 stags_quiz_score_form = form
#             elif request.GET.get('challenge') == 'games':
#                 games_challenge_score_form = form
#             elif request.GET.get('challenge') == 'sports':
#                 sports_challenge_score_form = form

#             context = {
#                 'forms': [
#                     (score_mitre_challenge_form, 'mitre'),
#                     (score_coding_challenge_form, 'coding'),
#                     (stags_quiz_score_form, 'stags'),
#                     (games_challenge_score_form, 'games'),
#                     (sports_challenge_score_form, 'sports'),
#                 ],
#                 'group': group,
#             }
#         return render(request, 'jumpstart/city-challenge.html', context)


@method_decorator(login_required, name='dispatch')
class MembersCheckInView(UserPassesTestMixin, View):
    """Update freshers' check in status.
       POST method only.
    """

    raise_exception = True


    def test_func(self):
        """Only helpers have access"""
        return is_helper(self.request.user)


    def post(self, request):
        """Update freshers' check in status.
           Only helpers can update check in status for members in their group during the event.
        """
        # check if update is unlocked
        jumpstart = get_current_site(request).jumpstart
        if not jumpstart.is_now:
            messages.error(request, 'Members check in status is locked. Failed to update members check in status.')
            return redirect('jumpstart:group')
        helper = Helper.objects.get(pk=request.user.username)
        # check if update is allowed
        group_members = helper.group.fresher_set.all()
        group_members_uuid = set(map(str, group_members.values_list('uuid', flat=True)))
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
            messages.error(request, 'Permission denined. Failed to update members check in status.')
        return redirect('jumpstart:group')
