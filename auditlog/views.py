from django.shortcuts import render

from .models import AuditLog


def view(request):
    auditlog = AuditLog.objects.all().order_by('-time', '-id')
    context = {
        'auditlog': auditlog,
    }
    return render(request, 'auditlog/view.html', context)
