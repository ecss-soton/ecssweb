from django.urls import path

from . import views

app_name='website'
urlpatterns = [
    path('', views.home, name='home'),

    # Events
    path('events/', views.events, name='events'),
    path('events/socials/', views.socials, name='socials'),
    path('events/gaming-socials/', views.gaming_socials, name='gaming-socials'),

    # Welfare
    path('welfare/', views.welfare, name='welfare'),

    # Sports
    path('sports/', views.sports, name='sports'),
    path('sports/football/', views.football, name='football'),
    path('sports/netball/', views.netball, name='netball'),
    path('sports/running/', views.running, name='running'),
    path('sports/others/', views.sports_others, name='sports_others'),

    # About
    path('contact/', views.contact, name='contact'),

    # Meta pages
    path('media-notice/', views.media_notice, name='media-notice'),
]
