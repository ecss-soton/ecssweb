from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from django.utils import timezone

from datetime import timedelta

class Command(BaseCommand):
    
    help = 'Clear non-persistent users did not login within the last 24 hours'

    def handle(self, *args, **options):
        users = User.objects.all()
        no_of_user_cleared = 0
        for user in users:
            if not user.samluser.is_persistent and timezone.now() > user.last_login + timedelta(hours=24):
                user.delete()
                no_of_user_cleared += 1
        self.stdout.write('Cleared {} user(s).'.format(no_of_user_cleared))
