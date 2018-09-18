import urllib.request, json
from datetime import datetime

from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from fbevents.models import Event


# Assume all the upcoming events are in the first page, paging is ignored
def sync_upcoming_events_with_fb():
    fb_events_api = 'https://graph.facebook.com/{}/events?access_token={}&fields=name,id,place,cover,start_time,end_time'.format(settings.FB_PAGE_ID, settings.FB_ACCESS_TOKEN)
    with urllib.request.urlopen(fb_events_api) as url:
        events = json.loads(url.read().decode())
        for event in events['data']:
            end_time = event.get('end_time', None)
            if end_time:
                end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
            else:
                start_time = datetime.strptime(event['start_time'], '%Y-%m-%dT%H:%M:%S%z')
            now = timezone.now()
            if (end_time and now < end_time) or now < start_time:
                defaults = {
                    'name': event['name'],
                    'location': event['place']['name'],
                    'cover': event['cover']['source'],
                    'start_time': event['start_time'],
                    'end_time': end_time,
                }
                Event.objects.update_or_create(fb_id=event['id'], defaults=defaults)

def get_upcoming_events():
    return Event.objects.filter(Q(end_time__gt=timezone.now()) | Q(start_time__gt=timezone.now())).order_by('start_time')
