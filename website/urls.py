from django.urls import path

from . import views

app_name='website'
urlpatterns = [
    path('', views.home, name='home'),
    #path('events/', views.events, name='events'),
]
