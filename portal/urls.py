from django.urls import path

from . import views

app_name='portal'
urlpatterns = [
    path('', views.overview, name='overview'),
    path('feedback/', views.feedback_submit, name='feedback-submit'),
    path('feedback/responses/', views.feedback_view, name='feedback-view'),
    path('feedback/respond/', views.feedback_respond, name='feedback-respond'),
]
