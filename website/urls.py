from django.urls import path

from . import views

app_name='website'
urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('events/socials/', views.events, name='socials'),
    path('events/game-socials/', views.events, name='game-socials'),
    path('welfare/', views.welfare, name='welfare'),
    path('media-notice/', views.media_notice, name='media-notice'),
]
