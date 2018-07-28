from django.urls import path

from . import views

app_name='feedback'
urlpatterns = [
    path('', views.submit, name='submit'),
    path('view/', views.view, name='view'),
    path('<int:feedback_id>/respond/', views.respond, name='respond'),
]