from django.contrib import admin
from django.contrib.auth.models import User, Permission


from .models import CommitteeRoleMember, Society, SocietyLink, Sponsor, SponsorLink


admin.site.unregister(User)
admin.site.register(Permission)


admin.site.register(CommitteeRoleMember)

admin.site.register(Society)
admin.site.register(SocietyLink)

admin.site.register(Sponsor)
admin.site.register(SponsorLink)
