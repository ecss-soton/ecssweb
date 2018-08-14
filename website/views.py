from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response


def home(request):
    return render(request, 'website/home.html')


# Events

def events(request):
    return render(request, 'website/events/events.html')


def socials(request):
    return render(request, 'website/events/socials.html')


def gaming_socials(request):
    return render(request, 'website/events/gaming-socials.html')


def jumpstart(request):
    return render(request, 'website/events/jumpstart.html')


# Welfare

def welfare(request):
    return render(request, 'website/welfare.html')


# Sports

def sports(request):
    return render(request, 'website/sports/sports.html')


def football(request):
    return render(request, 'website/sports/football.html')


def netball(request):
    return render(request, 'website/sports/netball.html')


def running(request):
    return render(request, 'website/sports/running.html')


def sports_others(request):
    return render(request, 'website/sports/others.html')


# About

def contact(request):
    return render(request, 'website/contact.html')


# Meta pages

def media_notice(request):
    return render(request, 'website/media-notice.html')


# Error pages

# 404
def page_not_found(request, exception):
    return render(request, 'website/error_pages/404.html', status=404)


# 403
def permission_denied(request, exception):
    return render(request, 'website/error_pages/403.html', status=403)


# 500
def server_error(request):
    return render(request, 'website/error_pages/500.html', status=500)
