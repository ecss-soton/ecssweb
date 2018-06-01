from django.urls import path

from . import views

app_name='auth'
urlpatterns = [
    path('saml/', views.auth_saml, name='auth_saml'),
    path('saml/metadata', views.saml_metadata, name='saml_metadata'),
    path('saml/acs', views.saml_acs, name='saml_acs'),
    path('saml/slo', views.saml_slo, name='saml_slo'),
    path('saml/test/', views.saml_test, name='saml_test'),
]
