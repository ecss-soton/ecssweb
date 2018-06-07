from django.urls import path

from . import views

app_name='ecsswebauth'
urlpatterns = [
    path('', views.auth, name='auth'),
    path('saml/login/', views.saml_login, name='saml_login'),
    path('saml/metadata', views.saml_metadata, name='saml_metadata'),
    path('saml/acs', views.saml_acs, name='saml_acs'),
    path('saml/logout/', views.saml_logout, name='saml_logout'),
    path('saml/test/', views.saml_test, name='saml_test'),
]
