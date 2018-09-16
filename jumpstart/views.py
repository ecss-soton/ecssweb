from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from .models import Fresher, Helper

from .utils import jumpstart_check


@method_decorator(login_required, name='dispatch')
class HomeView(UserPassesTestMixin, View):

    raise_exception = True

    def test_func(self):
        return jumpstart_check(self.request.user)

    def get(self, request):
        if Fresher.objects.filter(pk=request.user.username).exists():
            fresher = Fresher.objects.get(pk=request.user.username)
            context = {
                'fresher': fresher,
            }
            return render(request, 'jumpstart/fresher.html', context)
        elif Helper.objects.filter(pk=request.user.username).exists():
            helper = Helper.objects.get(pk=request.user.username)
            context = {
                'helper': helper,
            }
            return render(request, 'jumpstart/helper.html', context)
        elif request.user.groups.filter(name='committee').exists():
            pass
        else:
            raise PermissionDenied()