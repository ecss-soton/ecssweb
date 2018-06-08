from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

def home(request):
    return render(request, 'website/home.html')

def events_bbq(request):
    return render(request, 'website/events/bbq.html')

# 404
def page_not_found(request, exception):
    return render(request, 'website/error_pages/404.html', status=404)

# 403
def permission_denied(request, exception):
    return render(request, 'website/error_pages/403.html', status=403)

# 500
def server_error(request):
    return render(request, 'website/error_pages/500.html', status=500)
