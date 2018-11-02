from django.urls import path, re_path

from . import views

app_name='shop'
urlpatterns = [
    path('', views.shop, name='shop'),
    re_path(r'^(?P<sale>[\w-]+)/(?P<item>[\w-]+)/$', views.item, name='item'),
]
