from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from .models import AuditLog

@login_required
@permission_required('auditlog.view_auditlog', raise_exception=True)
def view(request):
    auditlog = AuditLog.objects.all().order_by('-time', '-id')
    context = {
        'auditlog': auditlog,
    }
    return render(request, 'auditlog/view.html', context)
