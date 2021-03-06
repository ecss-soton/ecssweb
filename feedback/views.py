from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.utils import timezone

from datetime import timedelta
import hashlib

from .models import Feedback, Response, SubmittedIpRecord, FeedbackAuditLog
from auditlog.models import AuditLog

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

def _get_ip_hash(request, times=100):
    ip = request.META.get('REMOTE_ADDR') # Works only if not behind a reverse proxy
    # Hash IP address 100 times
    ip_hash = hashlib.sha512(ip.encode('utf-8')).hexdigest()
    for i in range(0, times - 1):
        ip_hash = hashlib.sha512(ip_hash.encode('utf-8')).hexdigest()
    return ip_hash

# Check if the IP address exceeds daily feedback submission limit
def _is_not_exceed_submit_limit(ip_hash):
    # Delete SubmittedIpRecords older than a day
    SubmittedIpRecord.objects.filter(time__lt=timezone.now() - timedelta(hours=24)).delete()
    # Check if the IP address has already submitted 5 feedback within 24 hours
    return len(SubmittedIpRecord.objects.filter(ip_hash=ip_hash)) < 5

@login_required
def submit(request):
    if request.method == 'POST':
        # Check if the IP address exceeds daily feedback submission limit
        ip_hash = _get_ip_hash(request)
        if not _is_not_exceed_submit_limit(ip_hash):
            messages.error(request, 'Failed to submit feedback, one IP address can only submit 5 feedback within 24 hours. Please try again later.')
            return redirect('feedback:submit')

        # Build and check form
        submit_form = SubmitForm(request.POST)

        if submit_form.is_valid():

            # Save feedback
            feedback = submit_form.save(commit=False)
            # Record whether from a ECS user
            if request.user.has_perm('ecsswebauth.is_ecs_user'):
                feedback.from_ecs = True
            else:
                feedback.from_ecs = False
            # Record if a committee submission
            if request.user.has_perm('feedback.add_response'):
                feedback.committee = request.user.username
            feedback.save()

            # Record IP hash
            submitted_ip_record = SubmittedIpRecord(ip_hash=ip_hash)
            submitted_ip_record.save()

            if request.user.has_perm('feedback.add_response'):
                messages.success(request, 'Your feedback has been successfully submitted.')
            else:
                messages.success(request, 'Your feedback has been successfully submitted and saved anonymously.')
            return redirect('feedback:submit')

    else:

        # Check if back from successful submission
        msgs = get_messages(request)
        for msg in msgs:
            if msg.level == messages.SUCCESS:
                # If back from successful submission
                return render(request, 'feedback/submit_completed.html')
            if msg.level == messages.ERROR:
                # If back from failed submission
                return render(request, 'feedback/submit_failed.html')

        # Check if exceeded submission limit
        if not _is_not_exceed_submit_limit(_get_ip_hash(request)):
            return render(request, 'feedback/submit_limit_exceeded.html')

        submit_form = SubmitForm()

    context = {
        'submit_form': submit_form,
    }
    return render(request, 'feedback/submit.html', context)

@login_required
def view(request):
    # Show all feedback committee only, show feedback with response to everyone
    if request.user.has_perm('feedback.add_response'):
        feedbacks = Feedback.objects.all().order_by('-time', '-id')
    else:
        feedbacks = Feedback.objects.exclude(response__isnull=True).order_by('-time', '-id')

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
@permission_required('feedback.add_response', raise_exception=True)
def respond(request, feedback_uuid):
    feedback = get_object_or_404(Feedback, uuid=feedback_uuid)
    is_new = True
    if request.method == 'POST' and request.POST['submit'] != 'Delete':
        # Build form
        try:
            respond_form = RespondForm(request.POST, instance=feedback.response)
            is_new = False
        except Response.DoesNotExist:
            respond_form = RespondForm(request.POST)

        if respond_form.is_valid():
            # Save response and update who submitted the response
            response = respond_form.save(commit=False)
            response.feedback = feedback
            response.committee = request.user.username
            response.save()
            if is_new:
                action = 'create'
            else:
                action = 'edit'
            feedback_auditlog = FeedbackAuditLog(action=action, user=request.user.username, feedback=feedback)
            feedback_auditlog.save()
            auditlog = AuditLog(content_object=feedback_auditlog)
            auditlog.save()
            messages.success(request, 'Your response was saved successfully.')
            return redirect('feedback:view')

    elif request.method == 'POST' and request.POST['submit'] == 'Delete':
        try:
            response = feedback.response
            response.delete()
            feedback_auditlog = FeedbackAuditLog(action='delete', user=request.user.username, feedback=feedback)
            feedback_auditlog.save()
            auditlog = AuditLog(content_object=feedback_auditlog)
            auditlog.save()
            messages.success(request, 'The response has been deleted successfully.')
        except:
            messages.warning(request, 'The response requested to be deleted does not exist, nothing has been changed.')
        return redirect('feedback:view')

    else:

        # Build form
        try:
            respond_form = RespondForm(instance=feedback.response)
            is_new = False
        except Response.DoesNotExist:
            respond_form = RespondForm()
    
    context = {
        'feedback': feedback,
        'respond_form': respond_form,
        'is_new': is_new,
    }
    return render(request, 'feedback/respond.html', context)
