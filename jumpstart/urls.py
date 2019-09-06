from django.urls import path

from . import views

app_name='jumpstart'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('group/', views.HelperGroupView.as_view(), name='group'),
    path('profile/', views.HelperProfileView.as_view(), name='profile'),
    path('groups/', views.GroupsView.as_view(), name='groups'),
    path('city-challenge/edit/', views.CityChallengeEditView.as_view(), name='city-challenge-edit'),
    path('group-<int:group_id>/city-challenge/', views.CityChallengeView.as_view(), name='city-challenge'),
    path('scavenger-hunt/', views.ScavengerHuntView.as_view(), name='scavenger-hunt'),
    path('scavenger-hunt/edit/', views.ScavengerHuntEditView.as_view(), name='scavenger-hunt-edit'),
    path('members-check-in/', views.MemberCheckInView.as_view(), name='members-check-in'),
]
