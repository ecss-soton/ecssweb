from django.core.management.base import BaseCommand

from ...models import Fresher, Group

class Command(BaseCommand):
    """ python manage.py syncupcomingfbevents """

    help = 'Change fresher from one group to another'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('username', type=str)
        parser.add_argument('group_number', type=int)

    def handle(self, *args, **options):
        print(options['username'])
        fresher = Fresher.objects.get(pk=options['username'])
        print('You are about to move {}({}) from Group {} to Group {}'.format(fresher.username, fresher.name, fresher.group, options['group_number']))
        confirm = input('Type \'yes\' to continue, or \'no\' to cancel: ')
        if confirm == 'yes':
            fresher.group = Group.objects.get(pk=options['group_number'])
            fresher.save()
            print('Done')
