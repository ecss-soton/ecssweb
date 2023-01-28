from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms

import os
import uuid

from django.contrib.auth.models import Permission


def item_image_file_name(instance, filename):
    return ('shop/{}/{}-{}{}'.format(instance.item.sale.codename, instance.item.codename, uuid.uuid4(), os.path.splitext(filename)[1].lower()))


class Sale(models.Model):
    codename = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, verbose_name='sale name')
    start = models.DateTimeField(verbose_name='sale start time')
    end = models.DateTimeField(verbose_name='sale end time')


    @property
    def is_future(self):
        return self.start > timezone.now()


    @property
    def is_past(self):
        return self.end < timezone.now()


    @property
    def is_current(self):
        return not (self.is_future or self.is_past)


    def clean(self):
        if self.start >= self.end:
            raise ValidationError('End time should not be the same or earlier than start time.')


    def __str__(self):
        return self.name


    class Meta:
        ordering = ['start']


class Item(models.Model):
    codename = models.CharField(max_length=50)
    name = models.CharField(max_length=50, verbose_name='item name')
    description = models.TextField(verbose_name='item description')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='item price')
    sort_order = models.IntegerField(null=True, blank=True, verbose_name='item sort order')
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)

    paypal_button_id = models.CharField(max_length=50, verbose_name='item PayPal button ID')


    def __str__(self):
        return self.name


    class Meta:
        unique_together = ('sale', 'codename')

        ordering = ['sort_order']


class ItemOption(models.Model):

    AUTO_CHOICES = [
        ('username', 'Username'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    paypal_option_number = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)], verbose_name='PayPal option number')
    paypal_option_name = models.CharField(max_length=20, verbose_name='PayPal option name')
    name = models.CharField(max_length=20, verbose_name='item option name')
    auto_value = models.CharField(max_length=20, null=True, blank=True, choices=AUTO_CHOICES, verbose_name='auto value type')


    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('item', 'paypal_option_number')

        ordering = ['paypal_option_number']

class OptionChoice(models.Model):
    item_option = models.ForeignKey(ItemOption, on_delete=models.CASCADE)
    sort_order = models.IntegerField(null=True, blank=True, verbose_name='option choice sort order')
    name = models.CharField(max_length=150, verbose_name='option choice display name')
    value = models.CharField(max_length=20, verbose_name='option choice value')

    def __str__(self):
        return self.name

    
    class Meta:
        ordering = ['sort_order']

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=item_image_file_name, verbose_name='item image')
    sort_order = models.IntegerField(null=True, blank=True, verbose_name='item image sort order')
    item_options = models.ManyToManyField(OptionChoice, blank=True, null=True)

    class Meta:
        ordering = ['sort_order']

class ItemImageModelForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)

        if hasattr(self.instance, 'item'):
            self.fields['item_options'].queryset = OptionChoice.objects.filter(item_option__item=self.instance.item)
        else:
            self.fields['item_options'].queryset = OptionChoice.objects.all()

class ItemPermission(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.permission)

class Basket(models.Model):
    username = models.CharField(max_length=50)

    COLLECTION = 1
    UK_DELIVERY = 2
    DELIVERY = (
        (COLLECTION, 'Collection'),
        (UK_DELIVERY, 'UK Delivery')
    )

    delivery_option = models.IntegerField(choices=DELIVERY, default=COLLECTION)

    def total_price(self):
        price = 0

        for item in self.basketeditem_set.all():
            price += item.total_price()

        if self.should_include_delivery_cost():
            price += self.delivery_cost()

        return price

    def should_include_delivery_cost(self):
        return self.delivery_option == Basket.UK_DELIVERY

    def delivery_cost(self):
        price = 0

        for item in self.basketeditem_set.all():
            price += item.quantity * 5

        return price

class BasketedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    choices = models.ManyToManyField(OptionChoice)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def total_price(self):
        return self.item.price * self.quantity

class DeliveryAddress(models.Model):
    name = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=2, null=True)
    line1 = models.CharField(max_length=50, null=True)
    line2 = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)

class Transaction(models.Model):
    stripe_id = models.CharField(max_length=50, null=True)
    
    INITIATED = 1
    PROCESSED = 2
    TRANSCTION_STATUS = (
        (INITIATED, 'Open'),
        (PROCESSED, 'Processed')
    )

    status = models.IntegerField(choices=TRANSCTION_STATUS, default=INITIATED)

class Order(models.Model):
    username = models.CharField(max_length=50)
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    address = models.OneToOneField(
        DeliveryAddress,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    
    COLLECTION = 1
    UK_DELIVERY = 2
    DELIVERY = (
        (COLLECTION, 'Collection'),
        (UK_DELIVERY, 'UK Delivery')
    )

    delivery_option = models.IntegerField(choices=DELIVERY, default=COLLECTION)

    def total_price(self):
        price = 0

        for item in self.ordereditem_set.all():
            price += item.total_price()

        if self.delivery_option == Order.UK_DELIVERY:
            price += self.delivery_cost()

        return price

    def delivery_cost(self):
        price = 0

        for item in self.ordereditem_set.all():
            price += item.quantity * 5

        return price

    def separate_items(self):
        amount = 0

        for item in self.ordereditem_set.all():
            amount += item.quantity

        return amount

class OrderedItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    choices = models.ManyToManyField(OptionChoice)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def total_price(self):
        return self.item.price * self.quantity