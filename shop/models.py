from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

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
        return not (self.is_future() or self.is_past())

    
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


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=item_image_file_name, verbose_name='item image')
    sort_order = models.IntegerField(null=True, blank=True, verbose_name='item image sort order')


    class Meta:
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


class ItemPermission(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.permission)
