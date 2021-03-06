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

from .views import ProjectDetailView, ProjectCreateView, ProjectDeleteView, ProjectUpdateView, \
    ApplicantCreateView, ApplicantDeleteView, ApplicantStatusUpdateView

urlpatterns = [
    path('new', ProjectCreateView.as_view(), name='new'),
    path('<int:pk>', ProjectDetailView.as_view(), name='root'),
    path('<int:pk>/edit', ProjectUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete', ProjectDeleteView.as_view(), name='delete'),
    path('<int:project_id>/applications', TemplateView.as_view(template_name='applications.html'), name='applications'),
    path('applicant', ApplicantCreateView.as_view(),
         name='applicant_create'),
    path('applicant/<int:pk>/delete', ApplicantDeleteView.as_view(),
         name='applicant_delete'),
    path('applicant/<int:pk>/status', ApplicantStatusUpdateView.as_view(),
         name='applicant_status'),
]
