from django.contrib import admin
from django.contrib.auth.models import User, Permission


from .models import CommitteeRoleMember, Society, SocietyLink, Sponsor, SponsorLink
from ecsswebauth.models import EcsswebUserGroup


admin.site.unregister(User)
admin.site.register(Permission)

class CommitteeRoleMemberAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'role_codename': ('role_short_name',)
    }

admin.site.register(CommitteeRoleMember, CommitteeRoleMemberAdmin)

class EcsswebUserGroupAdmin(admin.ModelAdmin):
    search_fields = [
        'group__name',
    ]


admin.site.register(EcsswebUserGroup, EcsswebUserGroupAdmin)


class SocietyLinkInline(admin.StackedInline):
    model = SocietyLink
    extra = 0
    min_num = 0


class SocietyAdmin(admin.ModelAdmin):
    inlines = [
        SocietyLinkInline,
    ]


admin.site.register(Society, SocietyAdmin)


class SponsorLinkInline(admin.StackedInline):
    model = SponsorLink
    extra = 0
    min_num = 0


class SponsorAdmin(admin.ModelAdmin):
    inlines = [
        SponsorLinkInline,
    ]

admin.site.register(Sponsor, SponsorAdmin)
