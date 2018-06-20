from django.urls import path, include

from . import views

app_name='portal'
urlpatterns = [
    path('', views.overview, name='overview'),
]
