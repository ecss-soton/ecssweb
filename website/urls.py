from django.urls import path

from . import views

app_name='website'
urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('events/socials/', views.socials, name='socials'),
    path('events/gaming-socials/', views.gaming_socials, name='gaming-socials'),
    path('welfare/', views.welfare, name='welfare'),
    path('media-notice/', views.media_notice, name='media-notice'),
]
