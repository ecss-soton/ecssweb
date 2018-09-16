from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.exceptions import PermissionDenied

from .models import Fresher, Helper

from .forms import HelperEditProfileForm

from .utils import jumpstart_check, is_fresher, is_helper

from website.utils import is_committee


@method_decorator(login_required, name='dispatch')
class HomeView(UserPassesTestMixin, View):

    raise_exception = True

    def test_func(self):
        return jumpstart_check(self.request.user)

    def get(self, request):
        if is_fresher(request.user):
            fresher = Fresher.objects.get(pk=request.user.username)
            context = {
                'fresher': fresher,
            }
            return render(request, 'jumpstart/fresher.html', context)
        elif is_helper(request.user):
            helper = Helper.objects.get(pk=request.user.username)
            context = {
                'helper': helper,
            }
            return render(request, 'jumpstart/helper.html', context)
        elif is_committee(request.user):
            pass
        else:
            raise PermissionDenied()


@method_decorator(login_required, name='dispatch')
class ProfileEditView(UserPassesTestMixin, View):

    raise_exception = True

    def test_func(self):
        return jumpstart_check(self.request.user)

    def get(self, request):
        if is_fresher(request.user):
            pass
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
            pass
        elif is_helper(request.user):
            helper = Helper.objects.get(pk=request.user.username)

            profile_edit_form = HelperEditProfileForm(request.POST, request.FILES, instance=helper)

            if profile_edit_form.is_valid():
                profile_edit_form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('jumpstart:home')

            context = {
                'profile_edit_form': profile_edit_form,
            }
            return render(request, 'jumpstart/helper-profile-edit.html', context)
        else:
            raise Http404()
