from django.urls import path, re_path, reverse_lazy
from django.views.generic.base import RedirectView

from . import views

app_name='website'
urlpatterns = [
    path('', views.home, name='home'),

    path('jumpstart/', RedirectView.as_view(pattern_name='website:jumpstart-2018'), name='jumpstart-redirect'),

    # Societies
    path('societies/', RedirectView.as_view(url=reverse_lazy('website:societies', kwargs={'society': 'ecss'})), name='societies-default'),
    re_path(r'^societies/(?P<society>[\w-]+)/$', views.societies, name='societies'),

    # Sponsors
    path('sponsors/', views.sponsors, name='sponsors'),

    # Events
    path('events/', views.events, name='events'),
    path('events/socials/', views.socials, name='socials'),
    path('events/gaming-socials/', views.gaming_socials, name='gaming-socials'),
    path('events/jumpstart-2018/', views.jumpstart_2018, name='jumpstart-2018'),

    # Welfare
    path('welfare/', views.welfare, name='welfare'),

    # Sports
    path('sports/', views.sports, name='sports'),
    path('sports/football/', views.football, name='football'),
    path('sports/netball/', views.netball, name='netball'),
    path('sports/running/', views.running, name='running'),
    path('sports/others/', views.sports_others, name='sports_others'),

    # About
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Meta pages
    path('media-notice/', views.media_notice, name='media-notice'),
]
