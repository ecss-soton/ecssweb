from django.urls import path

from . import views

app_name='feedback'
urlpatterns = [
    path('', views.submit, name='submit'),
    path('view/', views.view, name='view'),
    path('<uuid:feedback_uuid>/respond/', views.respond, name='respond'),
]
