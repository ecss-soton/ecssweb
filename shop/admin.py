from django.contrib import admin

from .models import Sale, Item, ItemOption, ItemPermission, OptionChoice


class ItemInline(admin.StackedInline):
    model = Item
    extra = 0
    min_num = 0


class SaleAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]


class ItemOptionInline(admin.StackedInline):
    model = ItemOption
    extra = 0
    min_num = 0


class ItemPermissionInline(admin.StackedInline):
    model = ItemPermission
    extra = 0
    min_num = 0


class ItemAdmin(admin.ModelAdmin):
    inlines = [
        ItemOptionInline,
        ItemPermissionInline,
    ]


class OptionChoiceInline(admin.StackedInline):
    model = OptionChoice
    extra = 2
    min_num = 0


class ItemOptionAdmin(admin.ModelAdmin):
    inlines = [
        OptionChoiceInline,
    ]


admin.site.register(Sale, SaleAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemOption, ItemOptionAdmin)
