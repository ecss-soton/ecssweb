from django.contrib import admin

from .models import Election, Position


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

admin.site.register(Election, ElectionAdmin)
