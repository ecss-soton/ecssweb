from django.contrib import admin
from django.contrib.auth.models import User, Permission


from .models import CommitteeRoleMember, Society, SocietyLink, Sponsor, SponsorLink


admin.site.unregister(User)
admin.site.register(Permission)


admin.site.register(CommitteeRoleMember)


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
