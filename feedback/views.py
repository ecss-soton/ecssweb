from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Feedback

from .forms import SubmitForm, RespondForm

def _get_page_range(page_num, num_pages, adjacents):
    if adjacents * 2 + 1 >= num_pages:
        # Enough space to show all pages
        return range(1, num_pages + 1)

    begin = page_num - adjacents
    end = page_num + adjacents

    if begin <= 0:
        end -= (begin - 1)
        begin = 1
    elif end > num_pages:
        begin -= end - num_pages
        end = num_pages

    return range(begin, end + 1)

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

@login_required
def view(request):
    feedbacks = Feedback.objects.all().order_by('-time', '-id')

    # Show 10 feedback per page
    paginator = Paginator(feedbacks, 10)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    page_range = _get_page_range(page.number, paginator.num_pages, 3)

    context = {
        'feedbacks': page,
        'page_range': page_range
    }
    return render(request, 'feedback/view.html', context)

@login_required
def respond(request, feedback_id):
    if request.method == 'POST':
        return render(request, 'feedback/respond.html', context)
    else:
        feedback = get_object_or_404(Feedback, pk=feedback_id)

        # Build form
        respond_form = RespondForm()
        
    context = {
        'feedback': feedback,
        'respond_form': respond_form,
    }
    return render(request, 'feedback/respond.html', context)
