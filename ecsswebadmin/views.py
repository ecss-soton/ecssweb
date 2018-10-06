from django.shortcuts import render

from django.views.generic.base import RedirectView

from django.contrib.auth.mixins import UserPassesTestMixin

from urllib.parse import urlparse, parse_qsl, urlencode


class LoginRedirectView(UserPassesTestMixin, RedirectView):

    raise_exception = True

    def test_func(self):
        return not self.request.user.is_authenticated \
            or self.request.user.is_staff

    def get_redirect_url(self, *args, **kwargs):
        if 'next' in self.request.GET:
            return RedirectView.get_redirect_url(self, *args, **kwargs)
        else:
            url = RedirectView.get_redirect_url(self, *args, **kwargs)
            parse_url = urlparse(url)
            params = dict(parse_qsl(parse_url.query))
            params['next'] = '/admin/'
            url = '{}?{}'.format(parse_url.path, urlencode(params))
            return url
