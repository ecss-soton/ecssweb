from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.conf import settings

import yaml
import os

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
    context = {
        'sale': sale,
    }
    return render(request, 'shop/merch1819/merch1819.html', context)

@login_required
def merch1819_category(request, category):
    sale = get_object_or_404(Sale, codename='ecss-merch-2018-19')
    if sale.end < timezone.now():
        raise Http404()
    if sale.start > timezone.now() and not request.user.groups.filter(name='committee').exists():
        raise Http404()

    with open(os.path.join(settings.BASE_DIR, 'shop/data/merch1819.yaml')) as data_file:
        data = yaml.load(data_file)
        items = Item.objects.filter(Q(sale='ecss-merch-2018-19') & Q(codename__in=data[category]))

    category_names = {
        'tshirts': 'T-shirts',
        'hoodies': 'Hoodies',
        'sweatshirts': 'Sweatshirts',
    }

    category_name = category_names[category]

    context = {
        'sale': sale,
        'items': items,
        'category_name': category_name,
    }
    return render(request, 'shop/merch1819/category.html', context)
