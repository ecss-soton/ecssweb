from django.urls import path

from . import views

app_name='feedback'
urlpatterns = [
    path('', views.submit, name='submit'),
]
