from django.urls import path

from . import views

app_name='website'
urlpatterns = [
    path('', views.home, name='home'),
    path('media-notice/', views.media_notice, name='media_notice'),
    #path('events/', views.events, name='events'),
]
