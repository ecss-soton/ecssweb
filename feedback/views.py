from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def submit(request):
    return render(request, 'feedback/submit.html')
