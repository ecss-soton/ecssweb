from django.contrib import admin

from .models import Sale, Item, ItemImage, ItemOption, ItemPermission, OptionChoice, ItemImageModelForm, Order, OrderedItem, Transaction


class ItemInline(admin.StackedInline):
    model = Item
    extra = 0
    min_num = 0


class SaleAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end']

    prepopulated_fields = {
        'codename': ('name',),
    }

    inlines = [
        ItemInline,
    ]


class ItemImageInline(admin.StackedInline):
    form = ItemImageModelForm
    model = ItemImage
    extra = 0
    min_num = 0

    filter_horizontal = ('item_options',)


class ItemOptionInline(admin.StackedInline):
    model = ItemOption
    extra = 0
    min_num = 0

    prepopulated_fields = {
        'paypal_option_name': ('name',),
    }


class ItemPermissionInline(admin.StackedInline):
    model = ItemPermission
    extra = 0
    min_num = 0


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'sale']
    list_filter = ['sale__name']

    prepopulated_fields = {
        'codename': ('name',),
    }

    inlines = [
        ItemImageInline,
        ItemOptionInline,
        ItemPermissionInline,
    ]


class OptionChoiceInline(admin.StackedInline):
    model = OptionChoice
    extra = 2
    min_num = 0

    prepopulated_fields = {
        'value': ('name',),
    }


class ItemOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'item', 'get_sale_name']
    list_filter = ['item__name', 'item__sale__name']

    inlines = [
        OptionChoiceInline,
    ]

    prepopulated_fields = {
        'paypal_option_name': ('name',),
    }

    def get_sale_name(self, obj):
        return obj.item.sale.name
    get_sale_name.short_description = 'Sale'
    get_sale_name.admin_order_field = 'item__sale__start'

class OrderedItemInline(admin.StackedInline):
    model = OrderedItem
    extra = 0
    min_num = 0

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'stripe_id', 'status']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'created']

    inlines = [
        OrderedItemInline
    ]

admin.site.register(Sale, SaleAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemOption, ItemOptionAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Transaction, TransactionAdmin)