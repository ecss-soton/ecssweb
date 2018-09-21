from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.conf import settings

from .models import Fresher, Helper, Group

from .forms import HelperEditProfileForm, EditCityChallengeForm

from .utils import jumpstart_check, is_fresher, is_helper

from website.utils import is_committee

import requests
import json


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
            helper = Helper.objects.get(pk=request.user.username)
            groups = Group.objects.all().order_by('id')
            context = {
                'helper': helper,
                'groups': groups,
            }
            return render(request, 'jumpstart/helper.html', context)
        elif is_committee(request.user):
            groups = Group.objects.all().order_by('id')
            context = {
                'groups': groups,
            }
            return render(request, 'jumpstart/committee.html', context)
        else:
            raise PermissionDenied()


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

            city_challenge_edit_form = EditCityChallengeForm(request.POST, instance=group)

            if city_challenge_edit_form.is_valid():
                city_challenge_edit_form.save()
                messages.success(request, 'Your group\'s city challenge has been updated successfully.')
                return redirect('jumpstart:home')

            context = {
                'group': group,
                'city_challenge_edit_form': city_challenge_edit_form,
            }
            return render(request, 'jumpstart/city-challenge-edit.html', context)
        else:
            raise Http404()