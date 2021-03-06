"""hackncast URL Configuration

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

from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    # My apps
    url(r'^api/', include('modules.core.api.urls')),
    url(r'^api/user/', include('modules.user.api.urls')),
    url(r'^api/manage/', include('modules.manage.api.urls')),
    url(
        r'^admin/$',
        TemplateView.as_view(template_name="admin.html"), name='admin'
    ),
]

if settings.DEBUG and getattr(settings, 'SILK', False):
    urlpatterns += [
        url(r'^api/silk/', include('silk.urls', namespace='silk'))
    ]
