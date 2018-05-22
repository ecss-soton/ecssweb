from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'website/base.html')

def events_bbq(request):
    return render(request, 'website/events/bbq.html')
