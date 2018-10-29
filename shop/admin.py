from django.contrib import admin

from .models import Sale, Item, ItemImage, ItemOption, ItemPermission, OptionChoice


class ItemInline(admin.StackedInline):
    model = Item
    extra = 0
    min_num = 0


class SaleAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end']

    inlines = [
        ItemInline,
    ]


class ItemImageInline(admin.StackedInline):
    model = ItemImage
    extra = 0
    min_num = 0


class ItemOptionInline(admin.StackedInline):
    model = ItemOption
    extra = 0
    min_num = 0


class ItemPermissionInline(admin.StackedInline):
    model = ItemPermission
    extra = 0
    min_num = 0


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'sale']
    list_filter = ['sale__name']

    inlines = [
        ItemImageInline,
        ItemOptionInline,
        ItemPermissionInline,
    ]


class OptionChoiceInline(admin.StackedInline):
    model = OptionChoice
    extra = 2
    min_num = 0


class ItemOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'item', 'get_sale_name']
    list_filter = ['item__name', 'item__sale__name']

    inlines = [
        OptionChoiceInline,
    ]

    def get_sale_name(self, obj):
        return obj.item.sale.name
    get_sale_name.short_description = 'Sale'
    get_sale_name.admin_order_field = 'item__sale__start'


admin.site.register(Sale, SaleAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemOption, ItemOptionAdmin)
