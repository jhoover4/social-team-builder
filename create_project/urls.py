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
from django.urls import path

from django.views.generic import TemplateView
from .views import ProjectDetailView

urlpatterns = [
    path('new', TemplateView.as_view(template_name='project_new.html'), name='new'),
    path('<int:pk>', ProjectDetailView.as_view(), name='root'),
    path('<int:project_id>/edit', TemplateView.as_view(template_name='project_edit.html'), name='edit'),
    path('<int:project_id>/delete', TemplateView.as_view(template_name='project_edit.html'), name='delete'),
    path('<int:project_id>/applications', TemplateView.as_view(template_name='applications.html'), name='applications'),
]
