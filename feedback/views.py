from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required

from .forms import SubmitForm

@login_required
def submit(request):
    if request.method == 'POST':
        submit_form = SubmitForm(request.POST)

        if submit_form.is_valid():
            # If submission is valid
            submit_form.save()
            messages.success(request, 'Your feedback was submitted successfully.')
            return redirect('feedback:submit')

    else:

        # Check if back from successful submission
        msgs = get_messages(request)
        for msg in msgs:
            if msg.level == messages.SUCCESS and msg.message == 'Your feedback was submitted successfully.':
                # If back from successful submission
                return render(request, 'feedback/submit_completed.html')

        submit_form = SubmitForm()

    context = {
        'submit_form': submit_form,
    }
    return render(request, 'feedback/submit.html', context)
