from django.urls import path

from . import views

app_name='jumpstart'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('group/', views.GroupView.as_view(), name='group'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('group-helper/', views.FresherGroupHelperView.as_view(), name='group-helper'),
    path('groups/', views.CommitteeGroupsView.as_view(), name='groups'),
    path('groups/<int:group_number>/', views.CommitteeGroupView.as_view(), name='committee-group'),
    path('groups/import-export/', views.CommitteeGroupsImportExportView.as_view(), name='groups-import-export'),
    path('groups/helpers.csv', views.CommitteeGroupsHelpersExportView.as_view(), name='groups-helpers-export'),
    path('groups/freshers.csv', views.CommitteeGroupsFreshersExportView.as_view(), name='groups-freshers-export'),
    path('groups/helpers-import/', views.CommitteeGroupsHelpersImportView.as_view(), name='groups-helpers-import'),
    path('groups/freshers-import/', views.CommitteeGroupsFreshersImportView.as_view(), name='groups-freshers-import'),
    path('city-challenge/', views.CityChallengeView.as_view(), name='city-challenge'),
    path('scavenger-hunt/', views.ScavengerHuntView.as_view(), name='scavenger-hunt'),
    path('scavenger-hunt/scavenger-hunt.pdf', views.ScavengerHuntPdfView.as_view(), name='scavenger-hunt-pdf'),
    path('scavenger-hunt/<int:id>/', views.ScavengerHuntTaskView.as_view(), name='scavenger-hunt-task'),
    path('challenges/', views.CommitteeChallengesView.as_view(), name='committee-challenges'),
    path('members-check-in/', views.MembersCheckInView.as_view(), name='members-check-in'),
]
