from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Sale, Item


@login_required
def shop(request):
    sales = Sale.objects.all()
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
