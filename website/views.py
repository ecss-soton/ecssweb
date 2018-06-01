from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def home(request):
    return render(request, 'website/home.html')

def events_bbq(request):
    return render(request, 'website/events/bbq.html')
