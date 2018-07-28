"""ecssweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from ecsswebauth.views import saml_acs, saml_sls

urlpatterns = [
    path('', include('website.urls')),
    path('auth/', include('ecsswebauth.urls')),
    path('portal/', include('portal.urls')),
    path('portal/feedback/', include('feedback.urls')),
    path('portal/auditlog/', include('auditlog.urls')),
    # Temp for deployment
    path('https://society.ecs.soton.ac.uk/simplesaml/module.php/saml/sp/saml2-acs.php/default-sp', saml_acs, name='saml-asc'),
    path('simplesaml/module.php/saml/sp/saml2-logout.php/default-sp', saml_sls, name='saml-sls'),
]

handler404 = 'website.views.page_not_found'
handler403 = 'website.views.permission_denied'
handler500 = 'website.views.server_error'
