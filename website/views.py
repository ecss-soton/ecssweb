from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response


def home(request):
    return render(request, 'website/home.html')


def events(request):
    return render(request, 'website/events/events.html')


def socials(request):
    return render(request, 'website/events/socials.html')


def gaming_socials(request):
    return render(request, 'website/events/gaming-socials.html')


def welfare(request):
    return render(request, 'website/welfare.html')


def media_notice(request):
    return render(request, 'website/media-notice.html')


# 404
def page_not_found(request, exception):
    return render(request, 'website/error_pages/404.html', status=404)


# 403
def permission_denied(request, exception):
    return render(request, 'website/error_pages/403.html', status=403)


# 500
def server_error(request):
    return render(request, 'website/error_pages/500.html', status=500)
