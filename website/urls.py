from django.urls import path

from . import views

app_name='website'
urlpatterns = [
    path('', views.index, name='index'),
    path('events/bbq/', views.events_bbq, name='events_bbq'),
]