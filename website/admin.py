from django.contrib import admin

from .models import CommitteeRoleMember, Society, SocietyLink, Sponsor, SponsorLink


admin.site.register(CommitteeRoleMember)

admin.site.register(Society)
admin.site.register(SocietyLink)

admin.site.register(Sponsor)
admin.site.register(SponsorLink)
