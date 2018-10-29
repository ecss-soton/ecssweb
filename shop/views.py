from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from .models import Sale, Item


@login_required
def shop(request):
    if request.user.groups.filter(name='committee').exists():
        sales = Sale.objects.filter(end__gte=timezone.now())
    else:
        sales = Sale.objects.filter(Q(start__lte=timezone.now()) & Q(end__gte=timezone.now()))
    context = {
        'sales': sales,
    }
    return render(request, 'shop/shop.html', context)


@login_required
def item(request, sale, item):
    sale = get_object_or_404(Sale, codename=sale)
    item = get_object_or_404(Item, codename=item, sale=sale)
    context = {
        'item': item,
    }
    return render(request, 'shop/item.html', context)
