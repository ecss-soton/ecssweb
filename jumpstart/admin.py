from django.contrib import admin

from .models import Jumpstart, Group, Fresher, Helper


class JumpstartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start_time', 'end_time')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'helper')
    ordering = ('number',)
    search_fields = ('number', 'name')


    def helper(self, obj):
        return obj.helper.username


class HelperAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefered_name', 'username', 'group', 'has_photo')
    ordering = ('group',)
    search_fields = ('name', 'prefered_name', 'username')


    def has_photo(self, obj):
        return bool(obj.photo)
    has_photo.boolean = True

class FresherAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefered_name', 'username', 'group', 'is_checked_in')
    ordering = ('group', 'is_checked_in', 'name')
    search_fields = ('name', 'prefered_name', 'username')


admin.site.register(Jumpstart, JumpstartAdmin)

admin.site.register(Helper, HelperAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Fresher, FresherAdmin)
