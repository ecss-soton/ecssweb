from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from django.utils import timezone

from datetime import timedelta

class Command(BaseCommand):

    help = 'Clear non-persistent users did not login within the last 24 hours'

    def handle(self, *args, **options):
        users = User.objects.filter(last_login__lt=timezone.now() - timedelta(hours=24), samluser__is_persistent=False)
        no_of_user_cleared = len(users)
        users.delete()
        self.stdout.write('Cleared {} user(s).'.format(no_of_user_cleared))
