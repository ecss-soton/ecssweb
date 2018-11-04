from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from .models import Sale, Item


@login_required
def shop(request):
    if request.user.groups.filter(name='committee').exists():
        sales = Sale.objects.filter(end__gte=timezone.now()).order_by('start')
    else:
        sales = Sale.objects.filter(Q(start__lte=timezone.now()) & Q(end__gte=timezone.now())).order_by('start')
    context = {
        'sales': sales,
    }
    return render(request, 'shop/shop.html', context)


@login_required
def item(request, sale, item):
    sale = get_object_or_404(Sale, codename=sale)
    if sale.end < timezone.now():
        raise Http404()
    if sale.start > timezone.now() and not request.user.groups.filter(name='committee').exists():
        raise Http404()
    item = get_object_or_404(Item, codename=item, sale=sale)
    context = {
        'item': item,
    }
    return render(request, 'shop/item.html', context)


@login_required
def merch1819(request):
    sale = get_object_or_404(Sale, codename='ecss-merch-2018-19')
    if sale.end < timezone.now():
        raise Http404()
    if sale.start > timezone.now() and not request.user.groups.filter(name='committee').exists():
        raise Http404()
    context = {
        'sale': sale,
    }
    return render(request, 'shop/merch1819/merch1819.html', context)
