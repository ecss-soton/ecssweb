from django.db import models

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
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)

    paypal_button_id = models.CharField(max_length=50)

    def __str__(self):
        return '{} ({})'.format(self.name, self.sale.name)

    class meta:
        unique_together = ('sale, codename')


class ItemPermission(models.Model):
    item = models.ForeignKey(Sale, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT)

    def __str__(self):
        return '{} - {}'.format(self.item, self.permission)
