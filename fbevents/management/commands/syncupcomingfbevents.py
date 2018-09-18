from django.core.management.base import BaseCommand

from fbevents.utils import sync_upcoming_events_with_fb

class Command(BaseCommand):
    """ python manage.py syncupcomingfbevents """

    help = 'Sync upcoming events information with Facebook page events'

    def handle(self, *args, **options):
        sync_upcoming_events_with_fb()
