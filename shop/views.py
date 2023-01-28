from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.conf import settings

import yaml
import os

from .models import Sale, Item, Basket, BasketedItem, ItemOption, OptionChoice, Transaction, Order, OrderedItem, DeliveryAddress
from .utils import has_any_perms_item

import stripe
stripe.api_key = settings.SHOP_STRIPE_API_KEY

@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None
  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, settings.SHOP_STRIPE_ENDPOINT_KEY
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    # order id
    order_id = session.client_reference_id

    order = Order.objects.get(id=order_id)

    if(session.shipping_details is not None):
        address = DeliveryAddress.objects.create(
            name=session.shipping_details.name,
            city=session.shipping_details.address.city,
            country=session.shipping_details.address.country,
            line1=session.shipping_details.address.line1,
            line2=session.shipping_details.address.line2,
            postal_code=session.shipping_details.address.postal_code,
            state=session.shipping_details.address.state,
        )

        order.address = address
        order.save()

    if session.payment_status == "paid":
      order.transaction.status = Transaction.PROCESSED
      order.transaction.stripe_id = session.payment_intent
      
      order.transaction.save()

  return HttpResponse(status=200)

@login_required
def shop(request):
    # show all current and future sales for committee
    if request.user.groups.filter(name='committee').exists():
        sales = Sale.objects.filter(end__gte=timezone.now()).order_by('start')
    # only show current sales for other users
    else:
        sales = Sale.objects.filter(Q(start__lte=timezone.now()) & Q(end__gte=timezone.now())).order_by('start')
    context = {
        'sales': sales,
    }
    return render(request, 'shop/shop.html', context)

@login_required
def order(request, order):
    order = get_object_or_404(Order, id=order,transaction__status=Transaction.PROCESSED)
    
    context = {
        'order': order,
        'from_stripe': request.GET.get("from_stripe", False)
    }

    return render(request, 'shop/order.html', context)

@login_required
def orders(request):
    orders = Order.objects.filter(username=request.user,transaction__status=Transaction.PROCESSED).order_by('-id')
    
    context = {
        'orders': orders,
    }

    return render(request, 'shop/orders.html', context)

@login_required
def item(request, sale, item):
    sale = get_object_or_404(Sale, codename=sale)
    # do not show past sales items
    if sale.end < timezone.now():
        raise Http404()
    # only show future sales items to committee
    if sale.start > timezone.now() and not request.user.groups.filter(name='committee').exists():
        raise Http404()

    item = get_object_or_404(Item, codename=item, sale=sale)
    if not request.user.groups.filter(name='committee').exists() and not has_any_perms_item(request.user, item):
        raise Http404()
    context = {
        'item': item,
    }

    if request.method == "POST":
        # add to basket
        basket_obj,created = Basket.objects.get_or_create(username=request.user)

        basketedItem = BasketedItem.objects.create(item=item,basket=basket_obj,quantity=1)

        # get options
        for form_option_name in request.POST:
            if(form_option_name.startswith("os-")):
                optionId = form_option_name.replace("os-", "")
                optionValue = request.POST.get(form_option_name, -1)

                option = ItemOption.objects.get(id=optionId)
                optionChoice = OptionChoice.objects.get(item_option=option, id=optionValue)

                basketedItem.choices.add(optionChoice)

        return redirect('shop:basket')

    return render(request, 'shop/item.html', context)


@login_required
def basket(request):
    basket,created =Basket.objects.get_or_create(username=request.user)
    context = {
        'basket': basket,
    }

    if request.method == "POST":
        if request.POST['form_id'] == "item_edit":
            basketed_item_id = request.POST['item_id']
            basketed_item = BasketedItem.objects.get(id=basketed_item_id)

            if "delete" in request.POST:
                basketed_item.delete()
            elif "quantity" in request.POST:
                basketed_item.quantity = request.POST.get('quantity', 1)
                basketed_item.save(update_fields=["quantity"])
        elif request.POST['form_id'] == "delivery":
            basket.delivery_option = Basket.COLLECTION if request.POST.get('delivery', "collection") == "collection" else Basket.UK_DELIVERY
            basket.save(update_fields=["delivery_option"])
        elif request.POST['form_id'] == "checkout":
            # convert basket to order
            transaction = Transaction.objects.create()
            order = Order.objects.create(username=request.user,transaction=transaction,delivery_option=basket.delivery_option)

            stripe_items = []

            for item in basket.basketeditem_set.all():
                ordered_item = OrderedItem.objects.create(item=item.item, order=order, quantity=item.quantity)

                for choice in item.choices.all():
                    ordered_item.choices.add(choice)

                stripe_items.append({
                    'price': item.item.paypal_button_id,
                    'quantity': item.quantity
                })

            # provide shipping
            shipping_address_collection = {"allowed_countries": ["GB"]}
            shipping_options = [
                    {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": order.delivery_cost() * 100, "currency": "GBP"},
                        "display_name": "UK Delivery",
                    }
                    }
                ]

            if(order.delivery_option == Order.COLLECTION):
                shipping_address_collection = {}
                shipping_options = []

            # create checkout
            checkout_session = stripe.checkout.Session.create(
                line_items=stripe_items,
                mode='payment',
                success_url=settings.BASE_URL + '/portal/shop/order/' + str(order.id),
                cancel_url=settings.BASE_URL + '/portal/shop/basket',
                client_reference_id=order.id,
                customer_email=request.user.email,
                custom_text={
                    "submit": {"message": "We'll send you an email with your order details once payment has been processed."},
                },
                shipping_address_collection=shipping_address_collection,
                shipping_options=shipping_options,
            )

            # redirect user
            return redirect(checkout_session.url, code=303)

    return render(request, 'shop/basket.html', context)

@login_required
def add_to_basket(request, sale, item):
    sale = get_object_or_404(Sale, codename=sale)
    # do not show past sales items
    if sale.end < timezone.now():
        raise Http404()
    # only show future sales items to committee
    if sale.start > timezone.now() and not request.user.groups.filter(name='committee').exists():
        raise Http404()

    item = get_object_or_404(Item, codename=item, sale=sale)
    if not request.user.groups.filter(name='committee').exists() and not has_any_perms_item(request.user, item):
        raise Http404()
    
    basket,created = Basket.objects.get_or_create(username=request.user)
    baskedItem = BasketedItem.objects.create(item=item,basket=basket,quantity=1)

    context = {
        'basket': basket,
    }
    return render(request, 'shop/basket.html', context)

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
