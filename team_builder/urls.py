"""team_builder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import notifications.urls
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from . import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', TemplateView.as_view(template_name='search.html'), name='search'),
    path('profiles/', include(('user_profile.urls', 'user_profile'), namespace='profiles')),
    path('project/', include(('create_project.urls', 'create_project'), namespace='project')),
    path('admin/', admin.site.urls),
    url(r'^markdownx/', include('markdownx.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications'))
]

if settings.DEBUG:
    # for Django Debug Toolbar
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
