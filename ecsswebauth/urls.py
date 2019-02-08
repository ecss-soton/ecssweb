from django.urls import path

from . import views

app_name='ecsswebauth'
urlpatterns = [
    path('', views.auth, name='auth'),
    path('user.json', views.user_json, name='auth-user-json'),
    path('saml/login/', views.saml_login, name='saml-login'),
    path('saml/metadata', views.saml_metadata, name='saml-metadata'),
    path('saml/acs', views.saml_acs, name='saml-acs'),
    path('saml/logout/', views.saml_logout, name='saml-logout'),
    path('saml/sls', views.saml_sls, name='saml-sls'),
    path('saml/test/', views.saml_test, name='saml-test'),
]
