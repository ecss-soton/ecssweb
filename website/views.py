from django.shortcuts import render, get_object_or_404
from django.shortcuts import Http404
from django.conf import settings
from django.db.models import Q

from .models import Society, Sponsor, CommitteeRoleMember

from fbevents.utils import get_upcoming_events

import os
import yaml


# Homepage

def home(request):
    sponsors = Sponsor.objects.filter(Q(level='gold') | Q(level='silver') | Q(level='bronze'))
    context = {
        'sponsors': sponsors,
        'events': get_upcoming_events(),
    }
    return render(request, 'website/home.html', context)


# Committee

def committee_overview(request):
    committee = CommitteeRoleMember.objects.all()
    try:
        with open(os.path.join(settings.BASE_DIR, 'website/data/previous-committee.yaml')) as data_file:
            print("pain")
            previous_committees = yaml.load(data_file, Loader=yaml.FullLoader)
    except Exception as e:
        print(e)
    context = {
        'committee': committee,
        'previous_committees': previous_committees,
    }
    return render(request, 'website/committee/committee-overview.html', context)

def committee_member(request, role):
    committee = CommitteeRoleMember.objects.all()
    committee_role_member = get_object_or_404(CommitteeRoleMember, pk=role)
    context = {
        'committee': committee,
        'current_committee_member': committee_role_member,
    }
    return render(request, 'website/committee/committee-member.html', context)


# Societies

def societies(request):
    societies = Society.objects.all()
    context = {
        'societies': societies,
    }
    return render(request, 'website/societies/societies.html', context)

def societies_detail(request, society):
    societies = Society.objects.all()
    society_obj = get_object_or_404(Society, pk=society)
    context = {
        'society': society_obj,
        'societies': societies,
    }
    return render(request, 'website/societies/society.html', context)


# Sponsors

def _get_sponsors():
    gold_sponsors = Sponsor.objects.filter(level='gold')
    silver_sponsors = Sponsor.objects.filter(level='silver')
    bronze_sponsors = Sponsor.objects.filter(level='bronze')
    sixtyfourbit_sponsors = Sponsor.objects.filter(level='64-bit')
    thirtytwobit_sponsors = Sponsor.objects.filter(level='32-bit')
    sixteenbit_sponsors = Sponsor.objects.filter(level='16-bit')

    return gold_sponsors, silver_sponsors, bronze_sponsors, sixtyfourbit_sponsors, thirtytwobit_sponsors, sixteenbit_sponsors

def sponsors(request):
    if 'sponsor' in request.GET:
        sponsor = get_object_or_404(Sponsor, pk=request.GET['sponsor'])
        gold_sponsors, silver_sponsors, bronze_sponsors, sixtyfourbit_sponsors, thirtytwobit_sponsors, sixteenbit_sponsors = _get_sponsors()
        context = {
            'gold_sponsors': gold_sponsors,
            'silver_sponsors': silver_sponsors,
            'bronze_sponsors': bronze_sponsors,
            '64bit_sponsors': sixtyfourbit_sponsors,
            '32bit_sponsors': thirtytwobit_sponsors,
            '16bit_sponsors': sixteenbit_sponsors,
            'current_sponsor': sponsor,
        }
        return render(request, 'website/sponsors/sponsor.html', context)

    else:
        gold_sponsors, silver_sponsors, bronze_sponsors, sixtyfourbit_sponsors, thirtytwobit_sponsors, sixteenbit_sponsors = _get_sponsors()
        context = {
            'gold_sponsors': gold_sponsors,
            'silver_sponsors': silver_sponsors,
            'bronze_sponsors': bronze_sponsors,
            '64bit_sponsors': sixtyfourbit_sponsors,
            '32bit_sponsors': thirtytwobit_sponsors,
            '16bit_sponsors': sixteenbit_sponsors,
        }
        return render(request, 'website/sponsors/sponsors.html', context)

# Events

def events(request):
    return render(request, 'website/events/events.html')


def socials(request):
    return render(request, 'website/events/socials.html')


def gaming_socials(request):
    return render(request, 'website/events/gaming-socials.html')


def campus_hack_19(request):
    return render(request, 'website/events/campus-hack-19.html')


# Welfare

def welfare(request):
    return render(request, 'website/welfare.html')


# Sports

def sports(request):
    return render(request, 'website/sports/sports.html')


def football(request):
    try:
        with open(os.path.join(settings.BASE_DIR, 'website/data/football-positions.yaml')) as data_file:
            positions = yaml.load(data_file)
    except:
        raise Http404()
    context = {
        'positions': positions,
    }
    return render(request, 'website/sports/football.html', context)


def netball(request):
    return render(request, 'website/sports/netball.html')


def running(request):
    return render(request, 'website/sports/running.html')


def sports_others(request):
    return render(request, 'website/sports/others.html')


#  Freshers

def jumpstart_2018(request):
    return render(request, 'website/freshers/jumpstart-2018.html')


def freshers_2019(request):
    return render(request, 'website/freshers/freshers-2019.html')


def jumpstart_2019(request):
    return render(request, 'website/freshers/jumpstart-2019.html')


# About

def about(request):
    return render(request, 'website/about.html')


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
