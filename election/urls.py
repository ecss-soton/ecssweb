from django.urls import path, re_path

from . import views

app_name='election'

urlpatterns = [
    path('', views.elections, name='elections'),
    re_path(r'^(?P<election>[\w-]+)/$', views.election, name='election'),
    re_path(r'^(?P<election>[\w-]+)/(?P<position>[\w-]+)/$', views.PositionView.as_view(), name='position'),
    re_path(r'^(?P<election>[\w-]+)/(?P<position>[\w-]+)/nominate/$', views.NominationView.as_view(), name='nomination'),
    re_path(r'^(?P<election>[\w-]+)/(?P<position>[\w-]+)/support/$', views.SupportView.as_view(), name='support'),
]
