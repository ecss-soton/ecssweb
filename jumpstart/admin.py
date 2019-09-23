from django.contrib import admin

from .models import Jumpstart, Group, Fresher, Helper, ScavengerHuntTask


class JumpstartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start_time', 'end_time', 'helper_profile_lock_time')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'helper')
    search_fields = ('number', 'name')


    def helper(self, obj):
        return obj.helper.username


class HelperAdmin(admin.ModelAdmin):
    list_display = ('name', 'preferred_name', 'username', 'group', 'has_photo')
    search_fields = ('name', 'preferred_name', 'username')


    def has_photo(self, obj):
        return bool(obj.photo)
    has_photo.boolean = True

class FresherAdmin(admin.ModelAdmin):
    list_display = ('name', 'preferred_name', 'username', 'group', 'is_checked_in')
    search_fields = ('name', 'preferred_name', 'username')


admin.site.register(Jumpstart, JumpstartAdmin)

admin.site.register(Helper, HelperAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Fresher, FresherAdmin)

admin.site.register(ScavengerHuntTask)
