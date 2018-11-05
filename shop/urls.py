from django.urls import path, re_path

from . import views

app_name='shop'
urlpatterns = [
    # special sale pages
    path('ecss-merch-2018-19/', views.merch1819, name='merch1819'),
    re_path(r'^ecss-merch-2018-19/(?P<category>(tshirts|hoodies|sweatshirts))/$', views.merch1819_category, name='merch1819-category'),

    path('', views.shop, name='shop'),
    re_path(r'^(?P<sale>[\w-]+)/(?P<item>[\w-]+)/$', views.item, name='item'),
]
