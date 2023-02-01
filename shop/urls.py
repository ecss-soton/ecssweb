from django.urls import path, re_path

from . import views

app_name='shop'
urlpatterns = [
    # special sale pages
    path('ecss-merch-2018-19/', views.merch1819, name='merch1819'),
    re_path(r'^ecss-merch-2018-19/(?P<category>(tshirts|hoodies|sweatshirts))/$', views.merch1819_category, name='merch1819-category'),

    path('ecss-merch-2023/', views.merch2023, name='merch2023'),
    re_path(r'^ecss-merch-2023/(?P<category>(tshirts|hoodies|quarter-zips|jumpers|misc))/$', views.merch2023_category, name='merch2023-category'),

    path('orders', views.orders, name='orders'),
    re_path(r'^order/(?P<order>[\w-]+)/$', views.order, name='order'),

    path('', views.shop, name='shop'),
    re_path(r'^(?P<sale>[\w-]+)/$', views.shop, name='shop-sale'),
    re_path(r'^(?P<sale>[\w-]+)/(?P<item>[\w-]+)/$', views.item, name='item'),

    path('basket', views.basket, name='basket'),
    path('stripe_webhook', views.stripe_webhook)
]
