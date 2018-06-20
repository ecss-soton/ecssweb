from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SubmitForm

@login_required
def submit(request):
    submit_form = SubmitForm()
    context = {
        'submit_form': submit_form,
    }
    return render(request, 'feedback/submit.html', context)
