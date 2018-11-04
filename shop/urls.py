from django.urls import path, re_path

from . import views

app_name='shop'
urlpatterns = [
    path('', views.shop, name='shop'),
    re_path(r'^(?P<sale>[\w-]+)/(?P<item>[\w-]+)/$', views.item, name='item'),

    # special sale pages
    path('ecss-merch-2018-19/', views.merch1819, name='merch1819'),
    path('ecss-merch-2018-19/tshirts/', views.merch1819, name='merch1819'),
    path('ecss-merch-2018-19/hoodies/', views.merch1819, name='merch1819'),
    path('ecss-merch-2018-19/sweatshirts/', views.merch1819, name='merch1819'),
]
