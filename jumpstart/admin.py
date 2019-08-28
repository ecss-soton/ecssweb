from django.contrib import admin

from .models import Group, Fresher, Helper


class GroupAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'helper')
    ordering = ('number',)
    search_fields = ('number', 'name')


    def helper(self, obj):
        return obj.helper.username


class HelperAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefered_name', 'username', 'group')
    ordering = ('group',)
    search_fields = ('name', 'prefered_name', 'username')


    def helper(self, obj):
        return obj.helper.username


class FresherAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefered_name', 'username', 'group', 'is_checked_in')
    ordering = ('group', 'is_checked_in', 'name')
    search_fields = ('name', 'prefered_name', 'username')


admin.site.register(Helper, HelperAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Fresher, FresherAdmin)
