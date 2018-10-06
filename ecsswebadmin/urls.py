from django.urls import path, reverse_lazy

from django.views.generic.base import RedirectView

from django.conf import settings

from . import views

app_name='ecsswebadmin'
urlpatterns = [
    path('login/', views.LoginRedirectView.as_view(url=reverse_lazy(settings.LOGIN_URL), permanent=False, query_string=True), name='login'),
    path('logout/', views.RedirectView.as_view(url=reverse_lazy('ecsswebauth:saml-logout'), permanent=False), name='logout'),
    path('password_change/', views.RedirectView.as_view(url='https://subscribe.soton.ac.uk/ManagePassword/Change'), name='logout'),
]
