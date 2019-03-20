from django.contrib import admin

from .models import Election, Position, Nomination


class PositionInline(admin.StackedInline):
    model = Position
    extra = 0
    min_num = 0


class ElectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'voting_start', 'voting_end', 'nomination_start', 'nomination_end']

    prepopulated_fields = {
        'codename': ('name',),
    }

    inlines = [
        PositionInline,
    ]


class NominationAdmin(admin.ModelAdmin):
    list_display = ['name', 'nickname', 'position', 'position_election']
    list_filter = ['position__election']

    def position_election(self, nomination):
        return nomination.position.election


admin.site.register(Election, ElectionAdmin)
admin.site.register(Nomination, NominationAdmin)
