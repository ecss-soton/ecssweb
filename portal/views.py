from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def overview(request):
    return render(request, 'portal/overview.html')

@login_required
def feedback_submit(request):
    pass

@login_required
def feedback_view(request):
    pass

@login_required
def feedback_respond(request):
    pass
