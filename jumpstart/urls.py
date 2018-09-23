from django.urls import path

from . import views

app_name='jumpstart'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('groups/', views.GroupsView.as_view(), name='groups'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile-edit'),
    path('city-challenge/edit/', views.CityChallengeEditView.as_view(), name='city-challenge-edit'),
    path('group-<int:group_id>/city-challenge/', views.CityChallengeView.as_view(), name='city-challenge'),
]
