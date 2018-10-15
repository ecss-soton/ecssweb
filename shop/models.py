from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import Permission


class Sale(models.Model):
    codename = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name


class Item(models.Model):
    codename = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    sort_order = models.IntegerField(null=True, blank=True) 
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)

    paypal_button_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class meta:
        unique_together = ('sale, codename')


class ItemOption(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    paypal_on_number = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(7)])
    paypal_on_name = models.CharField(max_length=20)
    option_name = models.CharField(max_length=20)

    def __str__(self):
        return self.option_name

    class meta:
        unique_together = ('item, paypal_on_number')


class OptionChoice(models.Model):
    item_option = models.ForeignKey(ItemOption, on_delete=models.CASCADE)
    sort_order = models.IntegerField(null=True, blank=True)
    choice_name = models.CharField(max_length=20)
    choice_value = models.CharField(max_length=20)

    def __str__(self):
        return self.choice_name


class ItemPermission(models.Model):
    item = models.ForeignKey(Sale, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT)

    def __str__(self):
        return self.permission
