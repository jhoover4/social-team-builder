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
from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile-redirect', views.profile_redirect, name='profile_redirect'),
    path('<int:profile_id>', views.view_profile, name='root'),
    path('<int:profile_id>/dashboard', views.view_dashboard, name='user_dashboard'),
    path('edit', views.edit_profile, name='edit'),
    path('sign-up/', views.sign_up, name='sign_up'),
]
