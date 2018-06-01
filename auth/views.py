from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings

import json

from onelogin.saml2.auth import OneLogin_Saml2_Auth

def get_request_for_saml(request):
    result = {
        'https': 'on' if request.is_secure() else 'off',
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META['SERVER_PORT'],
        'get_data': request.GET.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.POST.copy()
    }
    return result

def init_saml(request):
    auth = OneLogin_Saml2_Auth(get_request_for_saml(request), custom_base_path=settings.SAML_FOLDER)
    return auth

# initiate saml login
def auth_saml(request):
    auth = init_saml(request)
    return HttpResponseRedirect(auth.login())

# sp metadata
def saml_metadata(request):
    auth = init_saml(request)
    saml_settings = auth.get_settings()
    metadata = saml_settings.get_sp_metadata()
    return HttpResponse(metadata, content_type='application/samlmetadata+xml')

# handle saml login response
@csrf_exempt
def saml_acs(request):
    auth = init_saml(request)
    auth.process_response()
    return HttpResponse(json.dumps(auth.get_attributes()))

# initiate logout
def saml_slo(request):
    auth = init_saml(request)
    return HttpResponseRedirect(auth.logout())

@login_required
def saml_test(request):
    return HttpResponse('hello')
