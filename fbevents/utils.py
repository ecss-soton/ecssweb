import urllib.request, json
from datetime import datetime

from django.utils import timezone
from django.conf import settings

from fbevents.models import Event


# Assume all the upcoming events are in the first page, paging is ignored
def sync_upcoming_events_with_fb():
    fb_events_api = 'https://graph.facebook.com/{}/events?access_token={}&fields=name,id,place,cover,start_time,end_time'.format(settings.FB_PAGE_ID, settings.FB_ACCESS_TOKEN)
    req = urllib.request.Request(fb_events_api)
    with urllib.request.urlopen(req) as url:
        events = json.loads(url.read().decode())
        for event in events['data']:
            end_time = datetime.strptime(event['end_time'], '%Y-%m-%dT%H:%M:%S%z')
            now = timezone.now()
            if now < end_time:
                defaults = {
                    'name': event['name'],
                    'location': event['place']['name'],
                    'cover': event['cover']['source'],
                    'start_time': event['start_time'],
                    'end_time': event['end_time'],
                }
                Event.objects.update_or_create(fb_id=event['id'], defaults=defaults)

def get_upcoming_events():
    return Event.objects.filter(end_time__gt=timezone.now())
